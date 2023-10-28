from django.db import models

from .Country import Country
from .Ubigeo import Ubigeo
from water_services_api.apps.core.models import TimeStampedModel

dir_storage = "configuration/people"


class Person(TimeStampedModel):
    full_name = models.CharField(max_length=140)
    country = models.ForeignKey(Country, related_name='country_person', blank=True, null=True,
                                on_delete=models.PROTECT)
    ubigeo = models.ForeignKey(Ubigeo, related_name='ubigeo_person',
                               blank=True, null=True, on_delete=models.PROTECT)
    url_instagram = models.CharField(max_length=500, blank=True, null=True)
    referrer = models.ForeignKey('self', related_name='referrer_person',
                                 blank=True, null=True, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to=dir_storage, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=dir_storage, blank=True, null=True)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        default_permissions = ()
        permissions = (
            ('view_person', 'Listar personas'),
            ('add_person', 'Agregar persona'),
            ('update_person', 'Actualizar persona'),
            ('delete_person', 'Eliminar persona'),
        )

    def __str__(self):
        return self.full_name
