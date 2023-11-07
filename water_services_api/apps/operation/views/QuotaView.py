from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from water_services_api.apps.operation.models.Quota import Quota
from water_services_api.apps.operation.permissions.Quota import QuotaPermissions as DisaryPermission
from water_services_api.apps.operation.serializers.Quota import QuotaSerializer
from water_services_api.apps.core.SearchFilter import search_filter
from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class QuotaViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer
    search_fields = ('client__person__fullname', 'client__person__first_name', 'client__person__last_name', 'month',
                     'year')
    ordering_fields = ('client__person__last_name', 'client__person__fullname', )
    filter_fields = ('client_id',)

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    @transaction.atomic
    def add(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data
                p = Quota.objects.create(**data)
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
            model = Quota.objects.get(pk=id)
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
            p = Quota.objects.filter(pk=int("%s" % (data['id']))).update(**data)
            model = Quota.objects.get(id=int("%s" % (data['id'])))
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
            Quota.objects.get(pk=id).delete()
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
            serializer = QuotaSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
