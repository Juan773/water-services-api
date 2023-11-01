import datetime

from django.contrib.auth.models import Permission, Group, User
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from oauth2_provider.models import get_application_model, get_access_token_model, get_refresh_token_model

from water_services_api.apps.configuration.models.Person import Person
from water_services_api.apps.configuration.models.Ubigeo import Ubigeo
from water_services_api.apps.configuration.serializers.Person import PersonBasicSerializer
from water_services_api.apps.configuration.serializers.Ubigeo import UbigeoListSerializer
from water_services_api.apps.core.FileUpload import FileUpload
from water_services_api.apps.core.HostValues import HostValues
from water_services_api.apps.core.InfoModels import PersonInfo
from water_services_api.apps.core.SearchFilter import keys_add_none
from water_services_api.apps.core.helpers import parse_error, parse_success
from water_services_api.apps.security.Auth import Auth
from water_services_api.apps.security.models.Module import Module
from water_services_api.apps.security.serializers.AccessToken import AccessTokenSerializer
from water_services_api.apps.security.serializers.Module import ModuleCustomSerializer

AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()


class FunctionsViewSet(viewsets.ViewSet):

    # DATOS DE UNA APLICACIÓN OAUTH
    @action(detail=False, methods=['post'], permission_classes=[],
            url_path='client_app', url_name='client_app')
    def client_app(self, request, format=None):
        name_app = request.data['name_app']
        Application = get_application_model()
        model = Application.objects.filter(
            name=name_app).values('client_id',
                                  'client_secret', 'authorization_grant_type', 'redirect_uris',
                                  'client_type').first()
        if (model):
            model['grant_type'] = model['authorization_grant_type']
            return Response(model)
        else:
            data = {
                'error': 'No encuentra aplicación cliente',
                'error_description': name_app + ' no está registrado en nuestro sistema de autenticación',
            }
            return Response(data, status=404)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='menu', url_name='menu')
    @transaction.atomic
    def menu(self, request, format=None):
        try:
            with transaction.atomic():
                user = request.user
                if user.is_superuser:
                    # modules = Module.objects.filter(level=1)
                    # data = ModuleChildrenSerializer(modules, many=True).data
                    modules = Module.objects.filter(level=1).order_by('order')
                    data = []
                    for item in modules:
                        obj = ModuleCustomSerializer(item).data

                        children = Module.objects.filter(parent_id=item.id, level=2).order_by(
                            'order')
                        children_array = []
                        for child in children:
                            child_data = ModuleCustomSerializer(child).data
                            children_ = Module.objects.filter(parent_id=child.id, level=3). \
                                order_by('order')
                            if len(children_) > 0:
                                child_data['children'] = ModuleCustomSerializer(children_, many=True).data
                            children_array.append(child_data)
                        if len(children_array) > 0:
                            obj['children'] = children_array
                        data.append(obj)
                else:
                    permissions = user.get_all_permissions()
                    # print(permissions)
                    ids_permissions = []
                    for p in permissions:
                        splitted = p.split(".")
                        f = Q(content_type__app_label=splitted[0], codename=splitted[1])
                        perm = Permission.objects.filter(f).values('id').first()
                        if perm:
                            ids_permissions.append(perm['id'])

                    # modules = Module.objects.filter(permission_id__in=ids_permissions, parent_id__isnull=False)
                    modules = Module.objects.filter(permission_id__in=ids_permissions).union(
                        Module.objects.filter(home=True))

                    dict_modules_level = {1: [], 2: [], 3: []}
                    for item in modules:
                        dict_modules_level[item.level].append(item.id)

                        parent_id = item.parent_id
                        if parent_id:
                            level = item.parent.level
                            if parent_id not in dict_modules_level[level]:
                                dict_modules_level[level].append(parent_id)

                            parent_id = item.parent.parent_id
                            if parent_id:
                                level = item.parent.parent.level
                                if parent_id not in dict_modules_level[level]:
                                    dict_modules_level[level].append(parent_id)

                    modules = Module.objects.filter(id__in=dict_modules_level[1]).order_by('order')
                    data = []
                    for item in modules:
                        obj = ModuleCustomSerializer(item).data

                        children = Module.objects.filter(parent_id=item.id, id__in=dict_modules_level[2]).order_by(
                            'order')
                        children_array = []
                        for child in children:
                            child_data = ModuleCustomSerializer(child).data
                            children_ = Module.objects.filter(parent_id=child.id, id__in=dict_modules_level[3]). \
                                order_by('order')
                            if len(children_) > 0:
                                child_data['children'] = ModuleCustomSerializer(children_, many=True).data
                            children_array.append(child_data)
                        if len(children_array) > 0:
                            obj['children'] = children_array
                        data.append(obj)
                result = parse_success(data)
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[],
            url_path='current_user', url_name='current_user')
    def current_user(self, request, format=None):
        user = request.user
        if user.id:
            per_id = user.person_id
            model = Person.objects.get(pk=per_id)
            dominio = HostValues.domain(request)
            if model.thumbnail:
                foto = dominio + model.logo.url
                foto_rec = dominio + model.thumbnail.url
            else:
                foto = dominio + "/media/configuration/people/pictures/img-default.png"
                foto_rec = foto
            data = {
                'thumbnail': foto_rec,
                'logo': foto,
                'first_name': model.person_natural_person.first_name.title(),
                'full_name': '%s %s' % (model.person_natural_person.first_name.title(),
                                        model.person_natural_person.father_last_name.title()),
                'person_id': per_id,
                'username': user.username
            }
            result = parse_success(data)
            return Response(result, status=status.HTTP_200_OK)
        else:
            error = parse_error('No autenticado correctamente')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='data_user_person', url_name='data_user_person')
    def data_user_person(self, request, format=None):
        user = request.user
        if user.id:
            per_id = user.person_id
            data = {}
            if per_id:
                data = PersonInfo(request, per_id)
            data['username'] = user.username
            data['email'] = user.email
            result = parse_success(data)
            return Response(result, status=status.HTTP_200_OK)
        else:
            error = parse_error('No autenticado correctamente')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='user_info_perfil', url_name='user_info_perfil')
    def user_info_perfil(self, request, format=None):
        user = request.user
        if user and user.id:
            applications = []
            per_id = user.person_id
            data = {}
            ubigeo = None
            referrer = None
            if per_id:
                data = PersonInfo(request, per_id)
                if data['ubigeo']:
                    ubigeo = Ubigeo.objects.get(pk=data['ubigeo'])
                if data['referrer']:
                    referrer = Person.objects.get(pk=data['referrer'])
            data['user_id'] = user.id
            data['person_id'] = per_id
            data['date_joined'] = user.date_joined
            data['is_active'] = user.is_active
            data['username'] = user.username
            data['email'] = user.email
            if data['ubigeo']:
                data['ubigeo'] = UbigeoListSerializer(ubigeo, many=False).data
            if data['referrer']:
                data['referrer'] = PersonBasicSerializer(referrer, many=False).data
            roles = []
            for p in user.groups.values():
                roles.append(p)
            data['roles'] = roles
            result = parse_success(data)
            return Response(result, status=status.HTTP_200_OK)
        else:
            error = parse_error('No autenticado correctamente')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='user_info_player', url_name='user_info_player')
    def user_info_player(self, request, format=None):
        id = request.query_params.get('id', None)
        user = User.objects.get(pk=id)
        if user and user.id:
            per_id = user.person_id
            data = {}
            ubigeo = None
            if per_id:
                data = PersonInfo(request, per_id)
                if data['ubigeo']:
                    ubigeo = Ubigeo.objects.get(pk=data['ubigeo'])
            data['date_joined'] = user.date_joined
            data['is_active'] = user.is_active
            data['username'] = user.username
            data['email'] = user.email
            if data['ubigeo']:
                data['ubigeo'] = UbigeoListSerializer(ubigeo, many=False).data
            result = parse_success(data)
            return Response(result, status=status.HTTP_200_OK)
        else:
            error = parse_error('No autenticado correctamente')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='change_password', url_name='change_password')
    def change_password(self, request, format=None):
        user = request.user
        data = request.data
        if user.id:
            id = user.id
            us = User.objects.get(pk=id)
            is_correct = us.check_password(data['current_password'])

            if is_correct:
                if data['password'] == data['confirm_password']:
                    us.set_password(data['password'])
                    us.password_gen = None
                    us.save()
                    result = parse_success({}, "Se cambió correctamente la contraseña")
                    return Response(result, status=status.HTTP_200_OK)
                else:
                    error = parse_error("La contraseñas no coinciden")
                    return Response(error, status=status.HTTP_403_FORBIDDEN)
            else:
                error = parse_error("La contraseña actual es incorrecta")
                return Response(error, status=status.HTTP_403_FORBIDDEN)
        else:
            error = parse_error('No autenticado correctamente')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='active_user', url_name='active_user')
    def active_user(self, request, format=None):
        data = request.data
        data_parse = keys_add_none(data, 'id')
        id = data_parse['id']
        user = User.objects.get(pk=id)
        if user.id:
            if user.is_active:
                error = parse_error("El usuario ya fue activado.")
                return Response(error, status=status.HTTP_403_FORBIDDEN)
            else:
                data_user = dict(
                    is_active='1'
                )
                User.objects.filter(pk=id).update(**data_user)
                result = parse_success({}, "Se activó correctamente.")
                return Response(result, status=status.HTTP_200_OK)
        else:
            error = parse_error('No autenticado correctamente')
            return Response(error, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='my_roles', url_name='my_roles')
    def my_roles(self, request, format=None):
        user = request.user
        data = []

        if user.is_superuser:
            add = dict(
                name='Es superusuario'
            )
            data.append(add)

        for p in user.groups.values():
            data.append(p)

        result = parse_success(data)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='mis_tokens', url_name='mis_tokens')
    def mis_tokens(self, request, format=None):
        user = request.user
        hoy = datetime.datetime.now()
        tokens = AccessToken.objects.filter(
            user_id=user.id,
            expires__gte=hoy
        ).order_by('-expires')

        data = AccessTokenSerializer(tokens, many=True).data

        result = parse_success(data)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[],
            url_path='create_new_account', url_name='create_new_account')
    def create_new_account(self, request, format=None):
        data = request.data

        email = data['email'].lower().strip()

        exist_email = User.objects.filter(email=email).values('id').first()
        if exist_email:
            result = dict(
                username=data['username'],
                idform='email',
                estado=False,
                mensaje='El email <b>%s</b> ya ha sido registrado, le sugerimos ingresar otro.' % (
                    email)
            )
            result = parse_success(result)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            exist_user = User.objects.filter(username=data['username']).values('id').first()
            if exist_user:
                result = dict(
                    username=data['username'],
                    idform='username',
                    estado=False,
                    mensaje='El usuario <b>%s</b> ya existe, le sugerimos ingresar otro.' % (
                        data['username'])
                )
                result = parse_success(result)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                if data['password'] == data['confirm_password']:
                    data_per = dict(
                        full_name=data['full_name'],
                        url_instagram=data['url_instagram'],
                        country_id='1',  # Peru
                        ubigeo_id=data['ubigeo_id'],
                        referrer_id=data['referrer_id']
                    )

                    pe = Person.objects.create(**data_per)
                    person_id = pe.id

                    data_us = dict(
                        username=data['username'],
                        person_id=person_id,
                        is_active='0',
                        is_staff='0',
                        is_superuser='0',
                        password=data['password'],
                        email=email,
                        password_change_at=datetime.datetime.now(),
                        date_new_change_at=timezone.now() + datetime.timedelta(days=365)
                    )

                    groups_default = Group.objects.filter(default=True).values_list('id', flat=True)
                    usu = User.objects.create_user(**data_us)
                    if groups_default:
                        usu.groups.set(groups_default)  # Roles por defecto
                    # usu.entities.set([3])  # Aplicacion HABITOS
                    usu.save()

                    if usu:
                        data_pa = dict(
                            id_app=data['id_app'],
                            person_id=person_id,
                            username=data['username'],
                            application_id=data['application_id']
                        )
                        token = Auth.create_token(person_id)['token']

                        result = dict(
                            id='correcto',
                            estado=True,
                            mensaje='Cuenta creada correctamente, bienvenido disfrute de su cuenta.',
                            access_token=token
                        )
                        self.save_logo_custom(person_id, request)
                        result = parse_success(result)
                        return Response(result, status=status.HTTP_200_OK)
                else:
                    result = dict(
                        username=data['username'],
                        idform='passNueva',
                        estado=False,
                        mensaje="Las <b>contraseñas</b> no coinciden. Verifique contraseñas ingresadas.",
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[],
            url_path='update_account', url_name='update_account')
    def update_account(self, request, format=None):
        request_data = request.data
        data = keys_add_none(request_data,
                             'user_id,email,password,confirm_password,person_id,full_name,url_instagram,'
                             'ubigeo_id,referrer_id,id_app,application_id,person_application_id')

        email = data['email'].lower().strip()

        exist_email = User.objects.filter(email=email).exclude(id=data['user_id']).values('id').first()
        if exist_email:
            result = dict(
                username=data['email'],
                idform='email',
                estado=False,
                mensaje='El email <b>%s</b> ya ha sido registrado, le sugerimos ingresar otro.' % (
                    email)
            )
            result = parse_success(result)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            data_per = dict(
                full_name=data['full_name'],
                url_instagram=data['url_instagram'],
                ubigeo_id=data['ubigeo_id'],
                referrer_id=data['referrer_id']
            )
            Person.objects.filter(pk=data['person_id']).update(**data_per)
            person_id = data['person_id']

            data_us = dict(
                # username=data['username'],
                # is_active='0',
                # is_staff='0',
                # is_superuser='0',
                # password=data['password'],
                email=email,
                # password_change_at=datetime.datetime.now(),
                # date_new_change_at=timezone.now() + datetime.timedelta(days=365)
            )
            User.objects.filter(pk=data['user_id']).update(**data_us)
            data_pa = dict(
                id_app=data['id_app'],
                application_id=data['application_id']
            )

            self.save_logo_custom(person_id, request)

            if data['password']:
                if data['password'] == data['confirm_password']:
                    data_us = dict(
                        # username=data['username'],
                        # is_active='0',
                        # is_staff='0',
                        # is_superuser='0',
                        password=data['password'],
                        # email=email,
                        password_change_at=datetime.datetime.now(),
                        date_new_change_at=timezone.now() + datetime.timedelta(days=365)
                    )
                    User.objects.filter(pk=data['user_id']).update(**data_us)
                else:
                    result = dict(
                        username=data['email'],
                        idform='passNueva',
                        estado=False,
                        mensaje="Las <b>contraseñas</b> no coinciden. Verifique contraseñas ingresadas.",
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

            result = dict(
                id='correcto',
                estado=True,
                mensaje='Cuenta creada correctamente, bienvenido disfrute de su cuenta.'
            )
            result = parse_success(result)
            return Response(result, status=status.HTTP_200_OK)

    def save_logo_custom(self, person_id, request):
        files = request.FILES
        if files and 'logo' in files:
            mode = Person.objects.filter(pk=person_id).values('logo', 'thumbnail').first()

            data_per = {
                'logo': FileUpload.configuration_person('logo', files['logo']),
                'thumbnail': FileUpload.configuration_person('thumbnail', files['logo'])
            }
            pe = Person.objects.filter(pk=person_id).update(**data_per)
            if pe and mode['logo']:
                FileUpload.delete_file(mode['logo'])
                FileUpload.delete_file(mode['thumbnail'])

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='data_user', url_name='data_user')
    def data_user(self, request, format=None):
        user = request.user
        data = dict(
            is_superuser=user.is_superuser,
            username=user.username,
            is_active=user.is_active
        )
        result = parse_success(data)
        return Response(result, status=status.HTTP_200_OK)
