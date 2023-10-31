from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from water_services_api.apps.configuration.models.Situation import Situation
from water_services_api.apps.configuration.permissions.Situation import SituationPermissions as DisaryPermission
from water_services_api.apps.configuration.serializers.Situation import SituationSerializer
from water_services_api.apps.core.SearchFilter import search_filter
from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class SituationViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = Situation.objects.all()
    serializer_class = SituationSerializer
    search_fields = ('name', 'code', )
    ordering_fields = ('code', 'name', )

    @action(detail=False, methods=['post'], permission_classes=[DisaryPermission, ],
            url_path='add', url_name='add')
    @transaction.atomic
    def add(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data
                p = Situation.objects.create(**data)
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
            model = Situation.objects.get(pk=id)
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
            p = Situation.objects.filter(pk=data['id']).update(**data)
            model = Situation.objects.get(id=data['id'])
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
            Situation.objects.get(pk=id).delete()
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
            serializer = SituationSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
