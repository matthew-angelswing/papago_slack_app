from django.http import HttpResponse
from django.conf import settings

def home(request):
    return HttpResponse(f"Hi! there? I'm Papago Slack App #{settings.SLACK_CLIENT_ID}")
