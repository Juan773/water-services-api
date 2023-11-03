from rest_framework import serializers

from water_services_api.apps.configuration.serializers.Person import PersonBasicSerializer
from water_services_api.apps.operation.models.Client import Client


class ClientSerializer(serializers.ModelSerializer):
    person = PersonBasicSerializer(many=False, read_only=True)

    class Meta:
        model = Client
        fields = ('id','person', 'client_type_id', 'situation_id', 'plan_id', 'block', 'lot', 'is_retired',
                  'is_finalized_contract', 'is_active')
