import datetime

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from water_services_api.apps.core.FileUpload import FileUpload
from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Payment import Payment, PaymentDetail
from water_services_api.apps.operation.models.Quota import Quota, QuotaDetail
from water_services_api.apps.operation.permissions.Payment import PaymentPermissions as DisaryPermission
from water_services_api.apps.operation.serializers.Payment import PaymentSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.helpers import parse_success, parse_error, get_total_month, update_total_month
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class PaymentViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    search_fields = ('client__person__first_name', 'client__person__last_name', 'client__person__full_name',
                     'client__person__document_number', 'client__block', 'client__lot', 'serie_payment', 'nro_payment',
                     'nro_operation')
    ordering_fields = ('date', 'client__person__last_name', 'client__person__full_name')

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    @transaction.atomic
    def add(self, request, *args, **kwargs):
        data = request.data
        is_different_date = False
        data_parse = keys_add_none(data, 'date,nro_operation,client_id,payment_method_id,is_active,quota_ids')
        if data_parse['date'] is None:
            data_parse['date'] = datetime.datetime.now()
            date_register = datetime.datetime.now().date().strftime("%Y-%m-%d")
        else:
            date_register = data_parse['date']

        date_now = datetime.datetime.now().date()
        date_pay = datetime.datetime.strptime(data_parse['date'], "%Y-%m-%d").date()

        if date_pay < date_now:
            is_different_date = True

        client = Client.objects.filter(pk=data_parse['client_id']).first()

        if client:
            if client.plan_id is None:
                result = dict(
                    estado=False,
                    mensaje='La persona no tiene un plan asignado.'
                )
                result = parse_success(result)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id

        quota_ids = data_parse['quota_ids'].split(',')
        quotas = Quota.objects.filter(client_id=data_parse['client_id'], id__in=quota_ids)
        if quotas.exists():
            min_quota = quotas.order_by('year_month')[0]
            count_min_q = Quota.objects.filter(client_id=data_parse['client_id'],
                                               year_month__lt=min_quota.year_month, is_paid=False).count()
            if count_min_q > 0:
                result = dict(
                    estado=False,
                    mensaje='Existen pagos anteriores sin cancelar.'
                )
                result = parse_success(result)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = dict(
                estado=False,
                mensaje='No existe el mes a cancelar.'
            )
            result = parse_success(result)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        quotas_details = QuotaDetail.objects.filter(quota_id__in=quota_ids)
        for item in quotas:
            if item.is_paid is True:
                result = dict(
                    estado=False,
                    mensaje='El pago del %s-%s ya fue realizado.' % (item.month, item.year)
                )
                result = parse_success(result)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            # verify total with total quota
            total = get_total_month(client.id, date_register, item.month, item.year)

            if total != item.total and is_different_date is False:
                result = dict(
                    estado=False,
                    mensaje='La mensualidad del %s-%s no esta procesado correctamente.' % (item.month,
                                                                                           item.year)
                )
                result = parse_success(result)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        ids = []
        list_add = []
        list_quota_update = []

        # Falta analizar cuando la fecha de pago fue antes de la fecha actual
        try:
            with transaction.atomic():
                for item in quotas:
                    if is_different_date is True:
                        update_total_month(client.id, date_register, item.month, item.year)
                        details = QuotaDetail.objects.filter(quota_id=item.id)
                    else:
                        details = quotas_details.filter(quota_id=item.id)
                    total = 0
                    for detail in details:
                        total = total + detail.amount

                    data_payment = dict(
                        date=data_parse['date'],
                        quota_id=item.id,
                        nro_operation=data_parse['nro_operation'],
                        client_id=data_parse['client_id'],
                        payment_method_id=data_parse['payment_method_id'],
                        user_id=user_id,
                        is_active=1,
                        total=total
                    )
                    p = Payment.objects.create(**data_payment)
                    for detail in details:
                        data_payment_detail = PaymentDetail(
                            payment_id=p.id,
                            service_id=detail.service_id,
                            gloss=detail.gloss,
                            quantity=detail.quantity,
                            cost=detail.cost,
                            amount=detail.amount,
                            order=detail.order
                        )
                        list_add.append(data_payment_detail)
                    self.save_file_operation(p.id, request)
                    item.is_paid = True
                    list_quota_update.append(item)
                    ids.append(p.id)

                PaymentDetail.objects.bulk_create(list_add)
                Quota.objects.bulk_update(list_quota_update, ["is_paid"])

                result = parse_success(
                    ids,
                    "Se agregó correctamente",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def save_file_operation(self, payment_id, request):
        files = request.FILES
        if files and 'file_operation' in files:
            mode = Payment.objects.filter(pk=payment_id).values('file_operation').first()

            data_payment = {
                'file_operation': FileUpload.operation_payment('file_operation', files['file_operation']),
            }
            pe = Payment.objects.filter(pk=payment_id).update(**data_payment)
            if pe and mode['file_operation']:
                FileUpload.delete_file(mode['file_operation'])

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='edit', url_name='edit')
    def edit(self, request):
        try:
            id = request.query_params.get('id', None)
            model = Payment.objects.get(pk=id)
            result = parse_success(self.get_serializer(model).data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='update', url_name='update')
    def update_(self, request, pk=None):
        data = request.data
        try:
            result = dict(
                estado=False,
                mensaje='No se ha desarrollado para editar el pago.'
            )
            result = parse_success(result)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

            # p = Payment.objects.filter(pk=int("%s" % (data['id']))).update(**data)
            # model = Payment.objects.get(id=int("%s" % (data['id'])))
            # result = parse_success(
            #     self.get_serializer(model).data, "Se actualizó correctamente"
            # )
            # return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='delete', url_name='delete')
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            PaymentDetail.objects.filter(payment_id=id).delete()
            Payment.objects.get(pk=id).delete()
            result = parse_success(id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='search', url_name='search')
    def search(self, request, *args, **kwargs):
        try:
            queryset = search_filter(self.get_queryset().distinct(), request)
            serializer = PaymentSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
