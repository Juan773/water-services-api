from django.db import models

from .Country import Country
from .UbigeoType import UbigeoType


class CountryUbigeoType(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    ubigeo_type = models.ForeignKey(UbigeoType, on_delete=models.PROTECT)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'Pais Tipo Ubigeo'
        verbose_name_plural = 'Paises Tipo Ubigeo'
        unique_together = ('country', 'ubigeo_type')
        default_permissions = ()
        permissions = (
            ('view_countryubigeotype',
             'Listar Paises Tipo Ubigeo'),
            ('add_countryubigeotype',
             'Agregar Paises Tipo Ubigeo'),
            ('update_countryubigeotype',
             'Actualizar Paises Tipo Ubigeo'),
            ('delete_countryubigeotype',
             'Eliminar Paises Tipo Ubigeo')
        )

    def __str__(self):
        return self.country_id
