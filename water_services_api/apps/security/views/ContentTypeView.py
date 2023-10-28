from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from water_services_api.apps.security.serializers.ContentType import ContentTypeSerializer
from water_services_api.apps.core.mixins import DefaultViewSetMixin
from water_services_api.apps.core.pagination import CustomPagination


class ContentTypeViewSet(CustomPagination, DefaultViewSetMixin, viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    search_fields = ('app_label', 'model', )

