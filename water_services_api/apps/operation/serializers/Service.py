from rest_framework import serializers

from water_services_api.apps.operation.models.Service import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
