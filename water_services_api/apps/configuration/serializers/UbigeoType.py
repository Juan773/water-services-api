from rest_framework import serializers

from water_services_api.apps.configuration.models.UbigeoType import UbigeoType


class UbigeoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoType
        fields = '__all__'


class UbigeoTypeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoType
        fields = ('id', 'code', 'name',)
