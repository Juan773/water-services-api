
from rest_framework import serializers

from water_services_api.apps.core.helpers import get_month_name
from water_services_api.apps.operation.models.Quota import Quota
from water_services_api.apps.operation.serializers.Client import ClientBasicSerializer
from water_services_api.apps.operation.serializers.Plan import PlanBasicSerializer


class QuotaSerializer(serializers.ModelSerializer):
    client = ClientBasicSerializer(many=False, read_only=True)
    plan = PlanBasicSerializer(many=False, read_only=True)
    month_name = serializers.SerializerMethodField()

    def get_month_name(self, q):
        month_name = get_month_name(q.month)
        return month_name.capitalize()

    class Meta:
        model = Quota
        fields = ('id', 'client', 'client_id', 'plan', 'plan_id', 'month', 'month_name', 'year', 'total', 'is_paid')


class QuotaBasicSerializer(serializers.ModelSerializer):
    client = ClientBasicSerializer(many=False, read_only=True)
    month_name = serializers.SerializerMethodField()

    def get_month_name(self, q):
        month_name = get_month_name(q.month)
        return month_name.capitalize()
    
    class Meta:
        model = Quota
        fields = ('id', 'client', 'client_id', 'plan_id', 'month', 'month_name', 'year', 'total', 'is_paid')
