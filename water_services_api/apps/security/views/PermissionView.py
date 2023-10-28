from django.contrib.auth.models import Permission
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from water_services_api.apps.security.permissions.Group import GroupPermissions as DisaryPermission
from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.security.serializers.Permission import PermissionSerializer, PermissionBasicSerializer, \
    PermissionEditSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class PermissionViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    search_fields = ('content_type__app_label', 'content_type__model', 'name', 'codename',)
    ordering_fields = ('content_type__app_label', 'content_type__model',
                       'codename', 'name', 'content_type__name',)

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    def add(self, request, *args, **kwargs):
        try:
            data = request.data
            perm = keys_add_none(data, 'name,content_type_id,codename')
            men = Permission.objects.create(**perm)
            result = parse_success({}, "Se registró correctamente")
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='edit', url_name='edit')
    def edit(self, request):
        try:
            id = request.query_params.get('id', None)
            model = Permission.objects.get(pk=id)
            result = parse_success(PermissionEditSerializer(model).data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='update', url_name='update')
    def update_(self, request, pk=None):
        try:
            data = request.data
            perm = keys_add_none(data, 'name,content_type_id,codename')
            Permission.objects.filter(pk=data['id']).update(**perm)
            result = parse_success({}, "Se actualizó correctamente")
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], permission_classes=[DisaryPermission, ],
            url_path='delete', url_name='delete')
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            Permission.objects.get(pk=id).delete()
            result = parse_success(id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[],
            url_path='search', url_name='search')
    def search(self, request, *args, **kwargs):
        try:
            queryset = search_filter(self.get_queryset(), request)
            serializer = PermissionBasicSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
