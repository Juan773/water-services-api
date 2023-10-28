from water_services_api.apps.configuration.models.Person import Person
from water_services_api.apps.configuration.serializers.Person import PersonSerializer
from water_services_api.apps.core.HostValues import HostValues


def PersonInfo(request, per_id):
    model = Person.objects.get(pk=per_id)
    domain = HostValues.domain(request)
    data = PersonSerializer(model).data
    if data['thumbnail']:
        data['thumbnail'] = domain + data['thumbnail']
        data['logo'] = domain + data['logo']

    return data
