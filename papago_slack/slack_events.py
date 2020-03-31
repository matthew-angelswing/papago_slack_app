from pprint import pprint

import hgtk
import requests

from django_simple_slack_app import slack_events, slack_commands
from . import papago


@slack_events.on("error")
def on_event_error(error):
    print("Error caused for ", end="")
    pprint(error)


@slack_events.on("oauth")
def on_event_error(user):
    print("OAuth finished for ", end="")
    pprint(user)


@slack_events.on("message")
def message_channels(event_data):
    pprint(event_data)
    event = event_data["event"]

    # event type checking
    if "text" not in event or "bot_id" in event or "subtype" in event:
        return

    # auth check user
    if "client" not in event or 'user' not in event:
        return

    user = event['user']
    if event['channel'] not in user.channels:
        return

    text = event["text"]

    # language checking
    if hgtk.checker.is_latin1(text):
        print("Translate %s characters to Korean" % len(text))
        translated = papago.translate(text, "en", "ko")
    else:
        print("Translate %s characters to English" % len(text))
        translated = papago.translate(text, "ko", "en")

    # translating
    if translated:
        new_text = "%s\n> %s" % (text, translated.replace("\n", "\n> "))
        response = event['client'].chat_update(
            channel=event["channel"], ts=event["ts"], text=new_text
        )
        assert response["ok"]


@slack_commands.on("error")
def on_command_error(error):
    pprint(error)


@slack_commands.on("/papago")
def papago_command(event_data):
    print("PAPAGO COMAMNDS!!!")
    pprint(event_data)


@slack_commands.on("/papago.on")
def papago_command(event_data):
    print("PAPAGO ON!!!")
    pprint(event_data)

    if 'user' in event_data:
        user = event_data['user']
        user.channels.append(event_data['channel_id'])
        user.save()

        requests.post(event_data['response_url'], json={
            "text": "Papago will translate on this channel for you!",
            "response_type": "ephemeral"
        })


@slack_commands.on("/papago.off")
def papago_command(event_data):
    print("PAPAGO OFF!!!")
    pprint(event_data)

    if 'user' in event_data:
        user = event_data['user']
        user.channels.remove(event_data['channel_id'])
        user.save()

        requests.post(event_data['response_url'], json={
            "text": "Papago translation is off!",
            "response_type": "ephemeral"
        })
