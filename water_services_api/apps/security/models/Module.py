from django.db import models
from django.contrib.auth.models import Permission, Group,User
from uuid import uuid4

from .Platform import Platform
from ...configuration.models.Person import Person
from ...core.models import TimeStampedModel

Group.add_to_class('default', models.BooleanField(default=False))
Group.add_to_class('code', models.CharField(max_length=30, null=True, blank=True))
User.add_to_class('password_change_at', models.DateTimeField(null=True, blank=True))
User.add_to_class('date_new_change_at', models.DateTimeField(null=True, blank=True))
User.add_to_class('person', models.OneToOneField(Person, related_name='user_person', blank=True, null=True, on_delete=models.PROTECT))

class Module(TimeStampedModel):
    platform = models.ForeignKey(Platform, related_name='module_platform', on_delete=models.PROTECT)
    expanded = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    home = models.BooleanField(default=False)
    code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=60)
    plural_title = models.CharField(max_length=70)
    link = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    target = models.CharField(max_length=60, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.PROTECT)
    order = models.IntegerField()
    level = models.IntegerField()
    permission = models.ForeignKey(Permission, related_name='module_permission', blank=True, null=True,
                                   on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Módulos'
        default_permissions = ()
        permissions = (
            ('view_module', 'Listado de módulos'),
            ('add_module', 'Agregar módulo'),
            ('update_module', 'Actualizar módulo'),
            ('delete_module', 'Eliminar módulo')
        )

    def __str__(self):
        return self.title
