from django.db import models

from water_services_api.apps.configuration.models.ClientType import ClientType
from water_services_api.apps.core.models import TimeStampedModel


class Plan(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    cost = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    mora = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    other_expenses = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    extension_days = models.DecimalField(max_digits=18, decimal_places=0, default=5)
    retired_extension_days = models.DecimalField(max_digits=18, decimal_places=0, default=5)
    reconnection_cost = models.DecimalField(max_digits=18, decimal_places=2, default=5)
    client_type = models.ForeignKey(ClientType, related_name='client_type_plan', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'
        default_permissions = ()
        permissions = (
            ('view_plan', 'Listar Planes'),
            ('add_plan', 'Agregar Planes'),
            ('update_plan', 'Actualizar Planes'),
            ('delete_plan', 'Eliminar Planes'),
        )

    def __str__(self):
        return self.name
