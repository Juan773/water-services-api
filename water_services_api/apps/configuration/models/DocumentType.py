from django.db import models


class DocumentType(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=60)
    code = models.CharField(blank=True, null=True, max_length=6, unique=True)
    pattern = models.CharField(max_length=60, blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de documentos'
        default_permissions = ()
        permissions = (
            ('view_documenttype',
             'Listar Tipos de documentos'),
            ('add_documenttype',
             'Agregar Tipos de documentos'),
            ('update_documenttype',
             'Actualizar Tipos de documentos'),
            ('delete_documenttype',
             'Eliminar Tipos de documentos'),
        )

    def __str__(self):
        return self.name
