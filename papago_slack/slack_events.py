from pprint import pprint

import hgtk
import slack

from django_slack_app import slack_events, slack_commands
from django_slack_app.models import SlackUserToken
from . import papago


@slack_events.on("message")
def message_channels(event_data):
    event = event_data["event"]

    # event type checking
    if "text" not in event or "bot_id" in event or "subtype" in event:
        return

    text = event["text"]
    user = event["user"]

    # language checking
    if hgtk.checker.is_latin1(text):
        print("Translate %s characters to Korean" % len(text))
        translated = papago.translate(text, "en", "ko")
    else:
        print("Translate %s characters to English" % len(text))
        translated = papago.translate(text, "ko", "en")

    # get user
    try:
        token = SlackUserToken.objects.get(user=user)
        client = slack.WebClient(token=token.token)
    except SlackUserToken.DoesNotExist:
        print(f"not registed user {user}")
        return

    # translating
    if translated:
        new_text = "%s\n> %s" % (text, translated.replace("\n", "\n> "))
        response = client.chat_update(
            channel=event["channel"], ts=event["ts"], text=new_text
        )
        assert response["ok"]


@slack_commands.on("/papago")
def papago_command(event_data):
    print("PAPAGO COMAMNDS!!!")
    pprint(event_data)
