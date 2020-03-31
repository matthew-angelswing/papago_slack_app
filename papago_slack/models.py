from django.db import models

from django_simple_slack_app.models import AbstractSlackUser


class ChannelsField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if not value:
            return []
        return list(map(str.strip, value.split(',')))

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if not value or not isinstance(value, str):
            return []

        return list(map(str.strip, value.split(',')))

    def get_prep_value(self, value):
        return ','.join(value)


class PapagoSlackUser(AbstractSlackUser):
    channels = ChannelsField("활성화된 채널들", default=[], null=False, blank=True)
