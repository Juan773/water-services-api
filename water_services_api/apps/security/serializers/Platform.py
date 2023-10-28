from rest_framework import serializers

from water_services_api.apps.security.models.Platform import Platform


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class PlatformBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name', 'code',)
