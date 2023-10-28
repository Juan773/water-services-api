from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.security.models.Platform import Platform
from water_services_api.apps.security.serializers.Platform import PlatformSerializer
from water_services_api.apps.core.SearchFilter import keys_add_none, search_filter
from water_services_api.apps.security.permissions.Platform import PlatformPermissions as DisaryPermission
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class PlatformViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    search_fields = ('name', 'code',)
    ordering_fields = '__all__'

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    def add(self, request, *args, **kwargs):
        try:
            data = request.data
            data_mod = keys_add_none(data, 'code,name,order')
            mod = Platform.objects.create(**data_mod)
            model = Platform.objects.get(pk=mod.id)
            result = parse_success(self.get_serializer(model).data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='edit', url_name='edit')
    def edit(self, request):
        try:
            id = request.query_params.get('id', None)
            model = Platform.objects.get(pk=id)
            result = parse_success(self.get_serializer(model).data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='update', url_name='update')
    def update_(self, request, pk=None):
        try:
            data = request.data
            data_mod = keys_add_none(data, 'code,name,order')

            Platform.objects.filter(pk=data['id']).update(**data_mod)
            model = Platform.objects.get(pk=data['id'])
            result = parse_success(self.get_serializer(model).data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], permission_classes=[DisaryPermission, ],
            url_path='delete', url_name='delete')
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            Platform.objects.filter(pk=id).update(deleted_at=datetime.today())
            result = parse_success(id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='search', url_name='search')
    def search(self, request, *args, **kwargs):
        try:
            queryset = search_filter(self.get_queryset(), request)
            serializer = PlatformSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
