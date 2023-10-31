from django.db import models


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(blank=True, null=True, max_length=6)

    class Meta:
        verbose_name = 'Metodo de pago'
        verbose_name_plural = 'Metodos de pago'
        default_permissions = ()
        permissions = (
            ('view_paymentmethod',
             'Listar Metodos de pago'),
            ('add_paymentmethod',
             'Agregar Metodos de pago'),
            ('update_paymentmethod',
             'Actualizar Metodos de pago'),
            ('delete_paymentmethod',
             'Eliminar Metodos de pago'),
        )

    def __str__(self):
        return self.name
