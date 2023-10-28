from django.db import models

from water_services_api.apps.core.models import TimeStampedBasicModel


class UbigeoType(TimeStampedBasicModel):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=50, unique=True)
    plural_name = models.CharField(max_length=60)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'Tipo Ubigeo'
        verbose_name_plural = 'Tipos de Ubigeos'
        default_permissions = ()
        permissions = (
            ('view_ubigeotype',
             'Listar Tipos de Ubigeos'),
            ('add_ubigeotype',
             'Agregar Tipos de Ubigeos'),
            ('update_ubigeotype',
             'Actualizar Tipos de Ubigeos'),
            ('delete_ubigeotype',
             'Eliminar Tipos de Ubigeos')
        )

    def __str__(self):
        return self.name
