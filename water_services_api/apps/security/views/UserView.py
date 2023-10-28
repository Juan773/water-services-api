from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from water_services_api.apps.core.SearchFilter import keys_add_none
from water_services_api.apps.core.helpers import parse_success, parse_error, str_to_array
from django.contrib.auth.models import User
from water_services_api.apps.security.permissions.User import UserPermissions as DisaryPermission
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination
from water_services_api.apps.security.serializers.User import UserSerializer
from water_services_api.apps.security.utils import Permissions
from water_services_api.apps.security.views.utils import get_modules_structure


class UserViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username', 'person__full_name')
    ordering_fields = ('person__logo', 'person__full_name', 'username', 'is_superuser',
                       'date_joined', 'is_active', 'email',
                       )

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    def add(self, request, *args, **kwargs):
        try:
            data = request.data
            data_us = keys_add_none(data, 'username,person_id,email,is_active,is_staff,is_superuser,password')
            if data_us['email']:
                exist_user = User.objects.filter(email=data_us['email']).values('id').first()
                if exist_user:
                    error = parse_error("El correo ingresado está en uso")
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            usu = User.objects.create_user(**data_us)
            model = User.objects.get(pk=usu.id)

            # create_staff(data_us['is_staff'], data_us['person_id'])
            result = parse_success(self.get_serializer(model).data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='edit', url_name='edit')
    def edit(self, request):
        id = request.query_params.get('id', None)
        model = User.objects.get(pk=id)
        data = self.get_serializer(model).data
        result = parse_success(data)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='update', url_name='update')
    def update_(self, request, pk=None):
        try:
            data = request.data
            data_us = keys_add_none(data, 'username,email,person_id,is_active,is_staff,is_superuser')

            if data_us['email']:
                exist_user = User.objects.filter(email=data_us['email']).exclude(id=data['id']).values('id').first()
                if exist_user:
                    error = parse_error("El correo ingresado está en uso")
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            User.objects.filter(id=data['id']).update(**data_us)
            model = User.objects.get(pk=data['id'])

            # create_staff(data['is_staff'], data['person_id'])
            result = parse_success(self.get_serializer(model).data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='delete', url_name='delete')
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            User.objects.filter(pk=id).update(is_active=False)
            result = parse_success(id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='change_password', url_name='change_password')
    def change_password(self, request, format=None):
        try:
            data = request.data
            if data['id']:
                id = data['id']
                us = User.objects.get(pk=id)
                us.set_password(data['password'])
                us.password_gen = None
                us.save()
                result = parse_success({}, "Correcto")
                return Response(result, status=status.HTTP_200_OK)
            else:
                error = parse_error('Usuario no encontrato')
                return Response(error, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='view_permissions', url_name='view_permissions')
    def view_permissions(self, request, pk=None):
        try:
            id = request.query_params.get('user_id', None)
            user = User.objects.get(pk=id)
            array_perms = []
            for item in user.get_all_permissions():
                array_perms.append(item.split('.')[1])
            perms = Permission.objects.filter(codename__in=array_perms).values_list('id', flat=True)
            result = get_modules_structure(perms, user.is_superuser)
            if result['status'] is True:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
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

            gr = User.objects.get(pk=data['user_id'])

            perms_id = []
            for item in gr.groups.all():
                perms_id.extend(item.permissions.values_list('id', flat=True))

            perms = Permission.objects.filter(id__in=perms_selected).exclude(id__in=perms_id)

            gr.user_permissions.set(perms)
            gr.save()
            result = parse_success(perms_selected)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='view_groups', url_name='view_groups')
    def view_groups(self, request, pk=None):
        try:
            id = request.query_params.get('user_id', None)
            model = User.objects.get(pk=id)
            groups = model.groups.values('id')

            listado1 = Group.objects.filter(id__in=groups).values()
            data = dict(
                roles=listado1,
            )
            result = parse_success(data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[DisaryPermission, ],
            url_path='change_group', url_name='change_group')
    def change_group(self, request, pk=None):
        try:
            data = request.data
            groups = []
            for p in data['roles']:
                groups.append(p['id'])

            gr = User.objects.get(pk=data['user_id'])
            gr.groups.set(groups)
            gr.save()
            result = parse_success(groups)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[DisaryPermission, ],
            url_path='delete_all_users', url_name='delete_all_users')
    def delete_all_users(self, request, *args, **kwargs):
        try:
            query = User.objects.exclude(username='admin').values('id')
            for p in query:
                User.objects.get(pk=p['id']).update(is_active=False)

            result = parse_success({}, "Correcto")
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='my_permissions', url_name='my_permissions')
    def my_permissions(self, request, pk=None):
        models = request.query_params.get('models', None)
        data = Permissions.accession(request, str_to_array(models))
        result = parse_success(data)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='is_super', url_name='is_super')
    def is_super(self, request):
        super_ = request.user.is_superuser
        result = parse_success({'super': super_})
        return Response(result, status=status.HTTP_200_OK)
