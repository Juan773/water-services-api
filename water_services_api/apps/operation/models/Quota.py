from django.db import models
from water_services_api.apps.core.models import TimeStampedModel
from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Plan import Plan
from water_services_api.apps.operation.models.Service import Service


class Quota(TimeStampedModel):
    client = models.ForeignKey(Client, related_name='client_quota', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='plan_quota', blank=True, null=True, on_delete=models.PROTECT)
    month = models.IntegerField()
    year = models.IntegerField()
    year_month = models.IntegerField()
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'
        default_permissions = ()
        permissions = (
            ('view_quota', 'Listar Cuotas'),
            ('add_quota', 'Agregar Cuotas'),
            ('update_quota', 'Actualizar Cuotas'),
            ('delete_quota', 'Eliminar Cuotas'),
        )

    def __str__(self):
        return "%s-%s %s" % (self.month, self.year, self.client.person.full_name)


class QuotaDetail(TimeStampedModel):
    quota = models.ForeignKey(Quota, related_name='quota_quota_detail', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='service_quota_detail', on_delete=models.PROTECT, blank=True,
                                null=True)
    gloss = models.CharField(max_length=1000)
    quantity = models.DecimalField(decimal_places=0, max_digits=18)
    cost = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'Cuota detalle'
        verbose_name_plural = 'Cuota detalles'
        default_permissions = ()
        permissions = (
            ('view_quotadetail', 'Listar Cuota detalles'),
            ('add_quotadetail', 'Agregar Cuota detalles'),
            ('update_quotadetail', 'Actualizar Cuota detalles'),
            ('delete_quotadetail', 'Eliminar Cuota detalles'),
        )

    def __str__(self):
        return "%s-%s %s" % (self.quota.month, self.quota.year, self.service.name)
