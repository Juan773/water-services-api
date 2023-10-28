from django.db import models

from water_services_api.apps.core.models import TimeStampedModel


class Country(TimeStampedModel):
    code = models.CharField(max_length=12, unique=True, blank=True, null=True)
    name = models.CharField(max_length=120, unique=True)
    abbreviation = models.CharField(max_length=30, blank=True, null=True)
    phone_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        default_permissions = ()
        permissions = (
            ('view_country',
             'Listado de paises'),
            ('add_country',
             'Agregar paises'),
            ('update_country',
             'Actualizar paises'),
            ('delete_country',
             'Eliminar paises')
        )

    def __str__(self):
        return self.name
