from rest_framework import serializers

from water_services_api.apps.operation.models.Client import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
