from rest_framework import serializers

from water_services_api.apps.operation.models.Plan import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
