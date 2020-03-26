from django.conf import settings
from django.http import HttpResponse


def home(request):
    return HttpResponse(f"Hi! there? I'm Papago Slack App #{settings.SLACK_CLIENT_ID}")
