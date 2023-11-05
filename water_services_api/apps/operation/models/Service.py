from django.db import models

from water_services_api.apps.core.models import TimeStampedModel


class Service(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    cost = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    code = models.CharField(blank=True, null=True, max_length=6, unique=True)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        default_permissions = ()
        permissions = (
            ('view_service', 'Listar Servicios'),
            ('add_service', 'Agregar Servicios'),
            ('update_service', 'Actualizar Servicios'),
            ('delete_service', 'Eliminar Servicios'),
        )

    def __str__(self):
        return self.name
