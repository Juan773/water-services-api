from django.db import models

from .Country import Country
from .UbigeoType import UbigeoType


class Ubigeo(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=70)
    ubigeo_type = models.ForeignKey(UbigeoType, related_name='ubigeo_type_ubigeo', on_delete=models.PROTECT)
    phone_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, related_name='country_ubigeo', on_delete=models.PROTECT)
    parent = models.ForeignKey('self', related_name='parent_ubigeo', blank=True, null=True,
                               on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Ubigeo'
        verbose_name_plural = 'Ubigeos'
        unique_together = ('country', 'name', 'ubigeo_type', 'parent')
        default_permissions = ()
        permissions = (
            ('view_ubigeo',
             'Listado de ubigeos'),
            ('add_ubigeo',
             'Agregar ubigeos'),
            ('update_ubigeo',
             'Actualizar ubigeos'),
            ('delete_ubigeo',
             'Eliminar ubigeos')
        )

    def __str__(self):
        return self.name
