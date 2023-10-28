from rest_framework import viewsets, permissions
from django.db.models.deletion import ProtectedError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from water_services_api.apps.configuration.models.UbigeoType import UbigeoType
from water_services_api.apps.configuration.permissions.UbigeoType import UbigeoTypePermissions as DisaryPermission
from water_services_api.apps.configuration.serializers.UbigeoType import UbigeoTypeSerializer, UbigeoTypeBasicSerializer
from water_services_api.apps.core.SearchFilter import search_filter
from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class UbigeoTypeViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = UbigeoType.objects.all()
    serializer_class = UbigeoTypeSerializer
    search_fields = ('name', 'code',)
    ordering_fields = '__all__'

    @action(url_path='add', url_name='add', methods=['post'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def add(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='edit', url_name='edit', methods=['get'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def edit(self, request):
        id = request.query_params.get('id', None)
        model = UbigeoType.objects.get(pk=id)
        return Response(self.get_serializer(model).data)

    @action(url_path='update', url_name='update', methods=['put'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def update_(self, request, pk=None):
        model = UbigeoType.objects.get(pk=request.data['id'])
        serializer = self.get_serializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='delete', url_name='delete', methods=['delete'],
            permission_classes=[DisaryPermission, ], detail=False, )
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            UbigeoType.objects.get(pk=id).delete()
            return Response({'status': True, 'id': id})
        except ProtectedError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path='search', url_name='search', methods=['get'],
            permission_classes=[permissions.IsAuthenticated, ], detail=False, )
    def search(self, request, *args, **kwargs):
        try:
            queryset = search_filter(self.get_queryset(), request)
            serializer = UbigeoTypeBasicSerializer(queryset, many=True)
            result = parse_success(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
