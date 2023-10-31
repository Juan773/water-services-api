from rest_framework import serializers

from water_services_api.apps.configuration.models.Situation import Situation


class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = '__all__'
