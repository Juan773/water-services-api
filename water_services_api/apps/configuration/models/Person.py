from django.db import models

from .Country import Country
from .DocumentType import DocumentType
from .Ubigeo import Ubigeo
from water_services_api.apps.core.models import TimeStampedModel

dir_storage = "configuration/people"


class Person(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='country_person', blank=True, null=True,
                                on_delete=models.PROTECT)
    ubigeo = models.ForeignKey(Ubigeo, related_name='ubigeo_person',
                               blank=True, null=True, on_delete=models.PROTECT, default=1)
    document_type = models.ForeignKey(DocumentType, related_name='document_type_person', blank=False, null=False,
                                      on_delete=models.PROTECT)
    document_number = models.CharField(max_length=20)
    phone_code = models.CharField(blank=True, null=True, max_length=3, default=51)
    phone_number = models.CharField(blank=True, null=True, max_length=10)
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
