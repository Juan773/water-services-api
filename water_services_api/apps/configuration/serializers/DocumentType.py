from rest_framework import serializers

from water_services_api.apps.configuration.models.DocumentType import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'


class DocumentTypeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name', 'code', 'pattern',)
