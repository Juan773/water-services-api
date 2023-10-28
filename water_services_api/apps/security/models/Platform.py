from django.db import models

from water_services_api.apps.core.models import TimeStampedModel


class Platform(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
        default_permissions = ()
        permissions = (
            ('view_platform', 'Listado de plataformas'),
            ('add_platform', 'Agregar plataforma'),
            ('update_platform', 'Actualizar plataforma'),
            ('delete_platform', 'Eliminar plataforma')
        )

    def __str__(self):
        return self.name
