from rest_framework import serializers

from water_services_api.apps.operation.models.Plan import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class PlanBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'name', 'cost', 'mora', 'other_expenses', 'reconnection_cost')
