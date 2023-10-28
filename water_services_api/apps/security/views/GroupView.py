from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.security.permissions.Group import GroupPermissions as DisaryPermission
from water_services_api.apps.security.serializers.Group import GroupSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination
from water_services_api.apps.security.views.utils import get_modules_structure


class GroupViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ('name', 'code',)
    ordering_fields = '__all__'

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    def add(self, request, *args, **kwargs):
        try:
            data = request.data
            default = keys_add_none(data, 'default')
            if default['default']:
                data_group = dict(
                    default='0'
                )
                Group.objects.filter(default=True).update(**data_group)
            serializer = self.get_serializer(data=data)
            serializer.is_valid()
            serializer.save()
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='edit', url_name='edit')
    def edit(self, request):
        try:
            id = request.query_params.get('id', None)
            model = Group.objects.get(pk=id)
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
            default = keys_add_none(data, 'default')
            if default['default']:
                data_group = dict(
                    default='0'
                )
                Group.objects.filter(default=True).update(**data_group)
            model = Group.objects.get(pk=data['id'])
            serializer = self.get_serializer(model, data=data)
            serializer.is_valid()
            serializer.save()
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], permission_classes=[DisaryPermission, ],
            url_path='delete', url_name='delete')
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            Group.objects.get(pk=id).delete()
            result = parse_success(id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='change_permission', url_name='change_permission')
    def change_permission(self, request, pk=None):
        try:
            data = request.data
            perms_selected = []
            for module in data['modules']:
                for child in module['children']:
                    for perm in child['actions']:
                        if perm['status'] is True:
                            perms_selected.append(perm['id'])
                for perm in module['actions']:
                    if perm['status'] is True:
                        perms_selected.append(perm['id'])

            gr = Group.objects.get(pk=data['rol_id'])
            gr.permissions.set(perms_selected)
            gr.save()
            result = parse_success(perms_selected)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='view_permissions', url_name='view_permissions')
    def view_permissions(self, request, pk=None):
        try:
            id = request.query_params.get('rol_id', None)
            permissions = Group.objects.filter(id=id).values_list('permissions', flat=True)
            result = get_modules_structure(permissions)
            if result['status'] is True:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[],
            url_path='search', url_name='search')
    def search(self, request, *args, **kwargs):
        try:
            queryset = search_filter(self.get_queryset(), request)
            serializer = self.get_serializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
