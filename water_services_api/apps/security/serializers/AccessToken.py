from rest_framework import serializers
from oauth2_provider.models import get_access_token_model, get_refresh_token_model

AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()
import datetime
import pytz

utc = pytz.UTC


class AccessTokenSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField('_created')
    expires = serializers.SerializerMethodField('_expires')

    def _created(self, obj):
        resul = dict(
            date=obj.created.strftime("%Y-%m-%d"),
            hour=obj.created.strftime("%H:%M:%S")
        )
        return resul

    def _expires(self, obj):
        now = datetime.datetime.now()
        today = datetime.datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            second=now.second,
            tzinfo=pytz.UTC)
        expires = datetime.datetime(
            year=obj.expires.year,
            month=obj.expires.month,
            day=obj.expires.day,
            hour=obj.expires.hour,
            minute=obj.expires.minute,
            second=obj.expires.second,
            tzinfo=pytz.UTC)
        active = True
        if today > expires:
            active = False

        result = dict(
            date=obj.expires.strftime("%Y-%m-%d"),
            hour=obj.expires.strftime("%H:%M:%S"),
            active=active
        )
        return result

    class Meta:
        model = AccessToken
        fields = ('id', 'token', 'created', 'expires', 'updated',)
