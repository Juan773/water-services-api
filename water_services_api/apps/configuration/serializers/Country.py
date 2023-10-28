from rest_framework import serializers

from water_services_api.apps.configuration.models.Country import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ('created_at', 'updated_at',)


class CountryBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'code', 'name', 'phone_code',)
