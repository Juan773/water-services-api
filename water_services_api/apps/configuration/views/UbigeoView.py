from rest_framework import viewsets
from django.db.models.deletion import ProtectedError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from water_services_api.apps.configuration.models.Ubigeo import Ubigeo
from water_services_api.apps.configuration.permissions.Ubigeo import UbigeoPermissions as DisaryPermission
from water_services_api.apps.configuration.serializers.Ubigeo import UbigeoSerializer, UbigeoListSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class UbigeoViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Ubigeo.objects.prefetch_related('ubigeo_type')
    serializer_class = UbigeoSerializer
    search_fields = ('name', 'code', 'ubigeo_type__name', 'parent__name', 'capital',)
    ordering_fields = ('ubigeo_type__name', 'code', 'name', 'parent__name', 'capital',)

    @action(url_path='add', url_name='add', methods=['post'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def add(self, request, *args, **kwargs):
        data = request.data
        columns = 'code,name,ubigeo_type_id,phone_code,country_id,region_natural_id'
        columns += ',capital,padre_id'
        data_re = keys_add_none(data, columns)
        p = Ubigeo.objects.create(**data_re)
        return Response(self.get_serializer(p).data)

    @action(url_path='edit', url_name='edit', methods=['get'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def edit(self, request):
        id = request.query_params.get('id', None)
        model = Ubigeo.objects.get(pk=id)
        return Response(self.get_serializer(model).data)

    @action(url_path='update', url_name='update', methods=['put'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def update_(self, request, pk=None):
        data = request.data
        columns = 'code,name,ubigeo_type_id,phone_code,country_id,region_natural_id'
        columns += ',capital,padre_id'
        data_re = keys_add_none(data, columns)
        p = Ubigeo.objects.filter(pk=data['id']).update(**data_re)
        model = Ubigeo.objects.get(id=data['id'])
        return Response(self.get_serializer(model).data)

    @action(url_path='delete', url_name='delete', methods=['delete'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            Ubigeo.objects.get(pk=id).delete()
            return Response({'status': True, 'id': id})
        except ProtectedError as e:
            return Response(ValidationError(e), status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='search', url_name='search', methods=['get'],
            permission_classes=[], detail=False, )
    def search(self, request, *args, **kwargs):
        try:
            queryset = search_filter(self.get_queryset().distinct(), request)
            complete = request.query_params.get('complete', None)
            if complete:
                serializer = self.get_serializer(queryset, many=True)
            else:
                serializer = UbigeoListSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

