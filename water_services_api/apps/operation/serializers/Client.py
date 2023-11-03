from rest_framework import serializers

from water_services_api.apps.configuration.serializers.Person import PersonBasicSerializer
from water_services_api.apps.core.HostValues import HostValues
from water_services_api.apps.operation.models.Client import Client


class ClientSerializer(serializers.ModelSerializer):
    person = PersonBasicSerializer(many=False, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'person', 'person_id', 'client_type_id', 'situation_id', 'plan_id', 'block', 'lot',
                  'is_retired', 'is_finalized_contract', 'is_active')


class ClientBasicSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    person_id = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'person_id', 'full_name', 'thumbnail', 'logo')

    def get_person_id(self, q):
        return q.person.id

    def get_full_name(self, q):
        return q.person.full_name

    def get_logo(self, q):
        foto = ""
        request = self.context.get('request')
        if request:
            dominio = HostValues.domain(request)
            if q.person.logo:
                foto = dominio + q.person.logo.url
            else:
                foto = ""
        return foto

    def get_thumbnail(self, q):
        foto = ""
        request = self.context.get('request')
        if request:
            dominio = HostValues.domain(request)
            if q.person.logo:
                if q.person.thumbnail:
                    foto = dominio + q.person.thumbnail.url
                else:
                    foto = ""
            else:
                foto = ""
        return foto