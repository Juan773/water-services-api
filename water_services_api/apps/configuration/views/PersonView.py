from datetime import datetime

import django_filters
from django.db import transaction
from django_filters import BaseInFilter, NumberFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from water_services_api.apps.configuration.permissions.Person import PersonPermissions as DisaryPermission
from water_services_api.apps.configuration.models.Person import Person
from water_services_api.apps.configuration.serializers.Person import PersonSearchSerializer, PersonSerializer, \
    PersonLogoSerializer, PersonBasicSerializer
from water_services_api.apps.configuration.serializers.Ubigeo import UbigeoListSerializer
from water_services_api.apps.core.FileUpload import FileUpload
from water_services_api.apps.core.SearchFilter import search_filter, keys_add_none

from water_services_api.apps.core.helpers import parse_error, parse_success
from water_services_api.apps.core.mixins import DefaultViewSetMixin, SearchViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class PersonSearchFilterSet(django_filters.FilterSet):
    id__in = NumberInFilter(field_name='id', lookup_expr='in', )
    id_exc__in = NumberInFilter(field_name='id', lookup_expr='in', exclude=True, )

    class Meta:
        model = Person
        fields = ('deleted_at',
                  'id__in',
                  'id_exc__in',
                  )


class PersonSearchViewSet(CustomPagination, SearchViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.prefetch_related().distinct()
    serializer_class = PersonSearchSerializer
    search_fields = ('full_name')
    ordering_fields = ('full_name',)
    filter_class = PersonSearchFilterSet


class PersonViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related()
    serializer_class = PersonSerializer
    search_fields = ('full_name',)
    ordering_fields = ('thumbnail', 'full_name', 'country__name',)
    filter_fields = ()

    @action(url_path='add', url_name='add', methods=['post'],
            permission_classes=[DisaryPermission, ], detail=False, )
    @transaction.atomic
    def add(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data

                data_per = keys_add_none(data, 'full_name,url_instagram,referrer_id,country_id,ubigeo_id')

                pe = Person.objects.create(**data_per)

                self.save_logo_custom(pe.id, request)
                result = parse_success(
                    self.get_serializer(pe).data,
                    "Se creó correctamente la persona",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='edit', url_name='edit', methods=['get'],
            permission_classes=[], detail=False, )
    def edit(self, request):
        try:
            with transaction.atomic():
                result = {}
                data = {}
                pk = request.query_params.get('id', None)
                model = Person.objects.get(pk=pk)

                data['id'] = pk
                data['country_id'] = model.country_id
                data['ubigeo_id'] = model.ubigeo_id

                if model.logo:
                    data['logo_url'] = request.build_absolute_uri(model.logo.url)
                else:
                    data['logo_url'] = None

                country = {}
                if model.country_id:
                    country['id'] = model.country_id
                    country['name'] = model.country.name
                    data['country'] = country

                if model.ubigeo_id:
                    data['ubigeo'] = UbigeoListSerializer(model.ubigeo).data

                referrer = {}
                if model.referrer_id:
                    referrer['id'] = model.referrer_id
                    referrer['name'] = model.referrer.full_name
                    data['referrer'] = referrer

                result = parse_success(data)
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

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

    @action(url_path='update', url_name='update', methods=['put'],
            permission_classes=[DisaryPermission, ], detail=False, )
    @transaction.atomic
    def update_(self, request):
        try:
            with transaction.atomic():
                data = request.data

                data_per = keys_add_none(data, 'full_name,url_instagram,referrer_id,country_id,ubigeo_id')
                Person.objects.filter(pk=data['id']).update(**data_per)
                model = Person.objects.get(id=data['id'])
                self.save_logo_custom(model.id, request)

                result = parse_success(
                    self.get_serializer(model).data,
                    "Se actualizó correctamente la persona",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='delete', url_name='delete', methods=['delete'],
            permission_classes=[DisaryPermission, ], detail=False, )
    @transaction.atomic
    def delete(self, request):
        try:
            with transaction.atomic():
                id = request.query_params.get('id', None)
                mode = Person.objects.filter(pk=id).values('logo', 'thumbnail').first()

                today = datetime.today()
                Person.objects.filter(pk=id).update(deleted_at=today)

                if mode and mode['logo']:
                    FileUpload.delete_file(mode['logo'])
                    FileUpload.delete_file(mode['thumbnail'])
                result = parse_success(
                    id,
                    "Se eliminó correctamente",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='search', url_name='search', methods=['get'],
            permission_classes=[], detail=False, )
    def search(self, request):
        queryset = search_filter(self.get_queryset().distinct(), request)
        serializer = PersonBasicSerializer(queryset, many=True, context={'request': request})
        result = parse_success(
            serializer.data
        )
        return Response(result, status=status.HTTP_200_OK)

    @action(url_path='save_logo', url_name='save_logo', methods=['post'],
            permission_classes=[], detail=False, )
    @transaction.atomic
    def save_logo(self, request):
        try:
            with transaction.atomic():
                files = request.FILES
                id = request.data['person_id']

                if files:
                    mode = Person.objects.filter(pk=id).values('logo', 'thumbnail').first()

                    data_per = {
                        'logo': FileUpload.configuration_person('logo', request.FILES['logo']),
                        'thumbnail': FileUpload.configuration_person('thumbnail', request.FILES['logo'])
                    }
                    pe = Person.objects.filter(pk=id).update(**data_per)
                    if pe and mode['logo']:
                        del1 = FileUpload.delete_file(mode['logo'])
                        del2 = FileUpload.delete_file(mode['thumbnail'])

                    model = Person.objects.get(pk=id)
                    result = parse_success(
                        PersonLogoSerializer(model).data,
                        "Se guardó el logo correctamente",
                    )
                    return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='delete_logo', url_name='delete_logo', methods=['post'],
            permission_classes=[], detail=False, )
    @transaction.atomic
    def delete_logo(self, request):
        try:
            with transaction.atomic():
                id = request.data['person_id']
                model = Person.objects.filter(pk=id).values('logo', 'thumbnail').first()
                del1 = FileUpload.delete_file(model['logo'])
                del2 = FileUpload.delete_file(model['thumbnail'])

                data_per = {'logo': None, 'thumbnail': None}
                pe = Person.objects.filter(pk=id).update(**data_per)
                model = Person.objects.get(pk=id)
                result = parse_success(
                    PersonLogoSerializer(model).data,
                    "Se eliminó el logo correctamente",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='view_info', url_name='view_info', methods=['get'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def view_info(self, request):
        result = {}
        data = {}
        pk = request.query_params.get('id', None)
        model = Person.objects.get(pk=pk)

        data['id'] = pk
        data['country_id'] = model.country_id
        data['ubigeo_id'] = model.ubigeo_id

        if model.logo:
            data['logo_url'] = request.build_absolute_uri(model.logo.url)
        else:
            data['logo_url'] = None

        country = {}
        if model.country_id:
            country['id'] = model.country_id
            country['name'] = model.country.name
            data['country'] = country

        if model.ubigeo_id:
            data['ubigeo'] = UbigeoListSerializer(model.ubigeo).data

        referrer = {}
        if model.referrer_id:
            referrer['id'] = model.referrer_id
            referrer['name'] = model.referrer.full_name
            data['referrer'] = referrer

        result = parse_success(data)
        return Response(result, status=status.HTTP_200_OK)

    @action(url_path='search_referrer', url_name='search_referrer', methods=['get'],
            permission_classes=[], detail=False, )
    def search_referrer(self, request):
        queryset = search_filter(self.get_queryset().distinct(), request)
        queryset = queryset.filter(person_person_application__isnull=False, user_person__is_active=True)
        serializer = PersonBasicSerializer(queryset, many=True)
        result = parse_success(
            serializer.data
        )
        return Response(result, status=status.HTTP_200_OK)

    @action(url_path='exist_person', url_name='exist_person', methods=['get'],
            permission_classes=[DisaryPermission, ], detail=False, )
    @transaction.atomic
    def exist_person(self, request):
        try:
            with transaction.atomic():
                full_name = request.query_params.get('full_name', None)
                full_name = str(full_name).lower().strip()
                print(full_name)
                count = Person.objects.filter(full_name__iexact=full_name).count()
                if count > 0:
                    person = Person.objects.filter(full_name__iexact=full_name).first()
                    result = parse_success(
                        self.get_serializer(person).data,
                        "",
                    )
                else:
                    result = parse_success(
                        "",
                        "No existe la persona",
                    )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
