import datetime

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Payment import Payment
from water_services_api.apps.operation.permissions.Payment import PaymentPermissions as DisaryPermission
from water_services_api.apps.operation.serializers.Payment import PaymentSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class PaymentViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    search_fields = ('client__full_name', )
    ordering_fields = ('client', )

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    @transaction.atomic
    def add(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data

                data_parse = keys_add_none(data, 'date,nro_operation,')
                if data_parse['date'] is None:
                    data_parse['date'] = datetime.datetime.now()

                plan_id = Client.objects.filter(pk=data_parse['client_id']).values('plan_id').first()

                if not plan_id:
                    result = dict(
                        plan_id=plan_id,
                        estado=False,
                        mensaje='La persona no tiene un plan asignado.'
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                user_id = request.user.id
                data_payment = dict(
                    date=data_parse['date'],
                    nro_operation=data_parse['nro_operation'],
                    client_id=data_parse['client_id'],
                    payment_method_id=data_parse['payment_method_id'],
                    plan_id=plan_id,
                    user_id=user_id
                )

                p = Payment.objects.create(**data)
                result = parse_success(
                    self.get_serializer(p).data,
                    "Se agregó correctamente",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

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
            p = Payment.objects.filter(pk=int(data['id']+'')).update(**data)
            model = Payment.objects.get(id=int(data['id']+''))
            result = parse_success(
                self.get_serializer(model).data, "Se actualizó correctamente"
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='delete', url_name='delete')
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
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
