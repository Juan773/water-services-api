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
from water_services_api.apps.operation.models.Plan import Plan
from water_services_api.apps.operation.models.Service import Service
from water_services_api.apps.operation.permissions.Payment import PaymentPermissions as DisaryPermission
from water_services_api.apps.operation.serializers.Payment import PaymentSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.helpers import parse_success, parse_error
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
        try:
            with transaction.atomic():
                data = request.data

                data_parse = keys_add_none(data, 'date,nro_operation,client_id,payment_method_id,is_active,month,year')
                if data_parse['date'] is None:
                    data_parse['date'] = datetime.datetime.now()

                client = Client.objects.filter(pk=data_parse['client_id']).first()

                if not client:
                    result = dict(
                        estado=False,
                        mensaje='La persona no tiene un plan asignado.'
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

                exist_pay = Payment.objects.filter(client_id=data_parse['client_id'], month=data_parse['month'],
                                                   year=data_parse['year'], is_active=True).values('id').first()
                if exist_pay:
                    result = dict(
                        estado=False,
                        mensaje='El pago del %s-%s ya fue realizado.' % (data_parse['month'], data_parse['year'])
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

                user_id = request.user.id
                data_payment = dict(
                    date=data_parse['date'],
                    month=data_parse['month'],
                    year=data_parse['year'],
                    nro_operation=data_parse['nro_operation'],
                    client_id=data_parse['client_id'],
                    payment_method_id=data_parse['payment_method_id'],
                    plan_id=client.plan_id,
                    user_id=user_id,
                    is_active=1
                )

                p = Payment.objects.create(**data_payment)

                plan = Plan.objects.filter(pk=client.plan_id).first()

                total = 0
                cost_associate = 0
                cost_user = 0
                if plan.client_type.code == 'socio':
                    cost_associate = plan.cost
                    total = total + cost_associate
                elif plan.client_type.code == 'user':
                    cost_user = plan.cost
                    total = total + cost_user

                data_payment_detail = dict(
                    payment_id=p.id,
                    service_id=None,
                    gloss='Cuota:Contrapest. por servicio agua-Socios',
                    quantity=1,
                    cost=cost_associate,
                    amount=cost_associate
                )
                PaymentDetail.objects.create(**data_payment_detail)
                data_payment_detail = dict(
                    payment_id=p.id,
                    service_id=None,
                    gloss='Cuota:Contrapest. por servicio agua-Usuarios',
                    quantity=1,
                    cost=cost_user,
                    amount=cost_user
                )
                PaymentDetail.objects.create(**data_payment_detail)

                reconnection_cost = 0
                if client.is_finalized_contract is False:
                    day = datetime.datetime.strptime(p.date, '%Y-%m-%d').date().day
                    if client.is_retired is False and plan.extension_days < day:
                        reconnection_cost = plan.reconnection_cost
                    elif client.is_retired is True and plan.retired_extension_days < day:
                        reconnection_cost = plan.reconnection_cost

                total = total + reconnection_cost

                data_payment_detail = dict(
                    payment_id=p.id,
                    service_id=None,
                    gloss='Corte/Reconexion',
                    quantity=1,
                    cost=reconnection_cost,
                    amount=reconnection_cost
                )
                PaymentDetail.objects.create(**data_payment_detail)

                mora = 0
                if client.is_finalized_contract is False:
                    day = datetime.datetime.strptime(p.date, '%Y-%m-%d').date().day
                    if client.is_retired is False and plan.extension_days < day:
                        mora = plan.reconnection_cost
                    elif client.is_retired is True and plan.retired_extension_days < day:
                        mora = plan.reconnection_cost

                total = total + mora

                data_payment_detail = dict(
                    payment_id=p.id,
                    service_id=None,
                    gloss='Mora',
                    quantity=1,
                    cost=mora,
                    amount=mora
                )
                PaymentDetail.objects.create(**data_payment_detail)

                if client.is_retired:
                    data_payment_detail = dict(
                        payment_id=p.id,
                        service_id=None,
                        gloss='Gastos administrativos',
                        quantity=1,
                        cost=plan.other_expenses,
                        amount=plan.other_expenses
                    )
                    PaymentDetail.objects.create(**data_payment_detail)
                    total = total + plan.other_expenses

                services = Service.objects.filter(is_active=True)
                for item in services:
                    data_payment_detail = dict(
                        payment_id=p.id,
                        service_id=item.id,
                        gloss=item.name,
                        quantity=1,
                        cost=item.cost,
                        amount=item.cost
                    )
                    PaymentDetail.objects.create(**data_payment_detail)
                    total = total + item.cost

                p.total = total
                p.save()
                self.save_file_operation(p.id, request)
                result = parse_success(
                    self.get_serializer(p).data,
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
