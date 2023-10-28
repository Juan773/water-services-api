from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.security.models.Module import Module
from water_services_api.apps.security.permissions.Module import ModulePermissions as DisaryPermission
from water_services_api.apps.security.serializers.Module import ModuleSerializer, ModuleEditSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class ModuleViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    search_fields = ('name', 'code', 'plural_name', 'parent__name', 'route',)
    ordering_fields = ('code', 'name', 'plural_name', 'route', 'parent__name', 'icon', 'permission__codename', 'order',)

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    @transaction.atomic
    def add(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data
                data_men = keys_add_none(data, 'platform_id,code,name,route,plural_name,icon,parent_id,order,level,'
                                               'type,permission_id')

                men = Module.objects.create(**data_men)
                result = parse_success(self.get_serializer(men).data)
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='edit', url_name='edit')
    def edit(self, request):
        try:
            id = request.query_params.get('id', None)
            model = Module.objects.get(pk=id)
            data = ModuleEditSerializer(model).data
            result = parse_success(data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='update', url_name='update')
    @transaction.atomic
    def update_(self, request, pk=None):
        try:
            with transaction.atomic():
                data = request.data
                data_men = keys_add_none(data,
                                         'platform_id,code,name,route,plural_name,icon,parent_id,order,'
                                         'level,type,permission_id')

                Module.objects.filter(id=data['id']).update(**data_men)
                model = Module.objects.get(pk=data['id'])
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
            Module.objects.get(pk=id).delete()
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
            serializer = ModuleSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
