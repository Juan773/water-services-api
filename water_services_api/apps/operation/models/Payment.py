from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max

from water_services_api import settings
from water_services_api.apps.configuration.models.PaymentMethod import PaymentMethod
from water_services_api.apps.core.models import TimeStampedModel
from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Plan import Plan
from water_services_api.apps.operation.models.Service import Service

dir_storage = "operation/payment"


class Payment(TimeStampedModel):
    client = models.ForeignKey(Client, related_name='client_payment', on_delete=models.PROTECT)
    date = models.DateTimeField()
    month = models.IntegerField()
    year = models.IntegerField()
    plan = models.ForeignKey(Plan, related_name='plan_payment', blank=True, null=True, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, related_name='payment_method_payment', on_delete=models.PROTECT)
    serie_payment = models.CharField(max_length=4)
    nro_payment = models.CharField(max_length=20)
    nro_operation = models.CharField(max_length=20, null=True, blank=True)
    file_operation = models.ImageField(null=True, blank=True, upload_to=dir_storage)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    user = models.ForeignKey(User, related_name='user_payment', blank=True, null=True,
                             on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.serie_payment = settings.SERIE_PAYMENT
        orders = Payment.objects.filter(serie_payment=settings.SERIE_PAYMENT)

        if orders.exists() and self._state.adding:
            max = orders.aggregate(Max('nro_payment'))
            new_nro = int(max['nro_payment__max']) + 1
            self.nro_payment = str(new_nro).zfill(settings.DIGITS_NRO_PAYMENT)
        elif self._state.adding:
            self.nro_payment = str(1).zfill(settings.DIGITS_NRO_PAYMENT)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        default_permissions = ()
        permissions = (
            ('view_payment', 'Listar Pagos'),
            ('add_payment', 'Agregar Pagos'),
            ('update_payment', 'Actualizar Pagos'),
            ('delete_payment', 'Eliminar Pagos'),
        )

    def __str__(self):
        return "%s-%s %s" % (self.serie_payment, self.nro_payment, self.client.person.full_name)


class PaymentDetail(TimeStampedModel):
    payment = models.ForeignKey(Payment, related_name='payment_payment_detail', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='service_payment_detail', on_delete=models.PROTECT, blank=True,
                                null=True)
    gloss = models.CharField(max_length=1000)
    quantity = models.DecimalField(decimal_places=0, max_digits=18)
    cost = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Pago detalle'
        verbose_name_plural = 'Pago detalles'
        default_permissions = ()
        permissions = (
            ('view_paymentdetail', 'Listar Pago detalles'),
            ('add_paymentdetail', 'Agregar Pago detalles'),
            ('update_paymentdetail', 'Actualizar Pago detalles'),
            ('delete_paymentdetail', 'Eliminar Pago detalles'),
        )

    def __str__(self):
        return "%s-%s %s" % (self.payment.serie_payment, self.payment.nro_payment, self.service.name)
