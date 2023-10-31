from django.contrib.auth.models import User
from django.db import models

from water_services_api.apps.configuration.models.ClientType import ClientType
from water_services_api.apps.configuration.models.Person import Person
from water_services_api.apps.configuration.models.Situation import Situation
from water_services_api.apps.core.models import TimeStampedModel
from water_services_api.apps.operation.models.Plan import Plan


class Client(TimeStampedModel):
    person = models.ForeignKey(Person, related_name='person_client', on_delete=models.PROTECT)
    client_type = models.ForeignKey(ClientType, related_name='client_type_client', blank=True, null=True,
                                    on_delete=models.PROTECT)
    situation = models.ForeignKey(Situation, related_name='situation_client', blank=True, null=True,
                                  on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='plan_client', blank=True, null=True,
                             on_delete=models.PROTECT)
    block = models.CharField(max_length=2, blank=True, null=True)
    lot = models.CharField(max_length=2, blank=True, null=True)
    user = models.ForeignKey(User, related_name='user_client', blank=True, null=True,
                             on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        default_permissions = ()
        permissions = (
            ('view_client', 'Listar Clientes'),
            ('add_client', 'Agregar Clientes'),
            ('update_client', 'Actualizar Clientes'),
            ('delete_client', 'Eliminar Clientes'),
        )

    def __str__(self):
        return self.person.full_name
