from rest_framework import serializers

from water_services_api.apps.configuration.models.ClientType import ClientType


class ClientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientType
        fields = '__all__'
