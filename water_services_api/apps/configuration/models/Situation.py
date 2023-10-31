from django.db import models


class Situation(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(blank=True, null=True, max_length=6, unique=True)

    class Meta:
        verbose_name = 'Situacion'
        verbose_name_plural = 'Situaciones'
        default_permissions = ()
        permissions = (
            ('view_situation',
             'Listar Situaciones'),
            ('add_situation',
             'Agregar Situaciones'),
            ('update_situation',
             'Actualizar Situaciones'),
            ('delete_situation',
             'Eliminar Situaciones'),
        )

    def __str__(self):
        return self.name
