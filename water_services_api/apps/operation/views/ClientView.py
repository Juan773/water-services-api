from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from water_services_api.apps.configuration.models.Person import Person
from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Plan import Plan
from water_services_api.apps.operation.permissions.Client import ClientPermissions as DisaryPermission
from water_services_api.apps.operation.serializers.Client import ClientSerializer
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none
from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class ClientViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    search_fields = ('person__first_name', 'person__last_name', 'person__full_name', 'person__document_number',
                     'block', 'lot',)
    ordering_fields = ('person__last_name', 'person__full_name')

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    @transaction.atomic
    def add(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data

                document_number = data['document_number'].strip()
                block = data['block'].strip()
                lot = data['lot'].strip()
                exist_document = Person.objects.filter(document_number__iexact=document_number).values('id').first()

                if exist_document:
                    result = dict(
                        document_number=data['document_number'],
                        estado=False,
                        mensaje='El documento <b>%s</b> ya ha sido registrado, le sugerimos ingresar otro.' % (
                            document_number)
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

                exist_block_lot = Client.objects.filter(block__iexact=block, lot__iexact=lot).values('id').first()

                if exist_block_lot:
                    result = dict(
                        block=data['block'],
                        lot=data['lot'],
                        estado=False,
                        mensaje='La manzana <b>%s</b> y el lote <b>%s</b> ya han sido registrados, le sugerimos '
                                'ingresar otros datos.' % (block, lot)
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                data_parse = keys_add_none(request.data, 'first_name,last_name,document_number,phone_number')
                document_type_id = None
                phone_code = None
                if data_parse['document_number'] is not None:
                    document_type_id = 1  # DNI
                if data_parse['phone_number'] is not None:
                    phone_code = '51',  # Codigo de Peru
                data_per = dict(
                    first_name=data_parse['first_name'],
                    last_name=data_parse['last_name'],
                    document_type_id=document_type_id,
                    document_number=data_parse['document_number'],
                    phone_code=phone_code,
                    phone_number=data_parse['phone_number'],
                    country_id='1',  # Peru
                    full_name="%s %s" % (data_parse['first_name'], data_parse['last_name'])
                )

                pe = Person.objects.create(**data_per)
                person_id = pe.id

                user_id = request.user.id

                client_type_id = Plan.objects.filter(pk=data['plan_id']).values('id').first()

                data_client = dict(
                    person_id=person_id,
                    client_type_id=client_type_id,
                    plan_id=data['plan_id'],
                    situation_id=data['situation_id'],
                    user_id=user_id,
                    block=data['block'],
                    lot=data['lot'],
                    is_retired=data['is_retired'],
                    is_active=data['is_active']
                )

                p = Client.objects.create(**data_client)
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
            model = Client.objects.get(pk=id)
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
            document_number = data['document_number'].strip()
            block = data['block'].strip()
            lot = data['lot'].strip()
            exist_document = Person.objects.filter(document_number__iexact=document_number)\
                .exclude(id=int("%s" % (data['person_id']))).values('id').first()

            if exist_document:
                result = dict(
                    document_number=data['document_number'],
                    estado=False,
                    mensaje='El documento <b>%s</b> ya ha sido registrado, le sugerimos ingresar otro.' % (
                        document_number)
                )
                result = parse_success(result)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            exist_block_lot = Client.objects.filter(block__iexact=block, lot__iexact=lot)\
                .exclude(id=int("%s" % (data['id']))).values('id').first()

            if exist_block_lot:
                result = dict(
                    block=data['block'],
                    lot=data['lot'],
                    estado=False,
                    mensaje='La manzana <b>%s</b> y el lote <b>%s</b> ya han sido registrados, le sugerimos '
                            'ingresar otros datos.' % (block, lot)
                )
                result = parse_success(result)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            data_parse = keys_add_none(request.data, 'first_name,last_name,document_number,phone_number')
            document_type_id = None
            phone_code = None
            if data_parse['document_number'] is not None:
                document_type_id = 1  # DNI
            if data_parse['phone_number'] is not None:
                phone_code = '51',  # Codigo de Peru
            data_per = dict(
                first_name=data_parse['first_name'],
                last_name=data_parse['last_name'],
                document_type_id=document_type_id,
                document_number=data_parse['document_number'],
                phone_code=phone_code,
                phone_number=data_parse['phone_number'],
                full_name="%s %s" % (data_parse['first_name'], data_parse['last_name'])
            )

            Person.objects.filter(pk=int("%s" % (data['person_id']))).update(**data_per)

            client_type_id = Plan.objects.filter(pk=data['plan_id']).values('id').first()

            data_client = dict(
                client_type_id=client_type_id,
                plan_id=data['plan_id'],
                situation_id=data['situation_id'],
                block=data['block'],
                lot=data['lot'],
                is_retired=data['is_retired'],
                is_active=data['is_active']
            )

            Client.objects.filter(pk=int("%s" % (data['id']))).update(**data_client)
            model = Client.objects.get(id=int("%s" % (data['id'])))
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
            Client.objects.get(pk=id).delete()
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
            serializer = ClientSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
