from django.db import models


class ClientType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(blank=True, null=True, max_length=6, unique=True)

    class Meta:
        verbose_name = 'Tipo de cliente'
        verbose_name_plural = 'Tipos de clientes'
        default_permissions = ()
        permissions = (
            ('view_clienttype',
             'Listar Tipos de clientes'),
            ('add_clienttype',
             'Agregar Tipos de clientes'),
            ('update_clienttype',
             'Actualizar Tipos de clientes'),
            ('delete_clienttype',
             'Eliminar Tipos de clientes'),
        )

    def __str__(self):
        return self.name
