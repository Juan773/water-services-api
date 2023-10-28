from rest_framework import serializers

from water_services_api.apps.configuration.models.Ubigeo import Ubigeo
from water_services_api.apps.configuration.serializers.Country import CountryBasicSerializer
from water_services_api.apps.configuration.serializers.UbigeoType import UbigeoTypeBasicSerializer


class Ubigeo2Serializer(serializers.ModelSerializer):
    ubigeo_type = UbigeoTypeBasicSerializer(many=False, read_only=True)

    class Meta:
        model = Ubigeo
        fields = '__all__'


class UbigeoSerializer(serializers.ModelSerializer):
    ubigeo_type_name = serializers.CharField(source='ubigeo_type.name', required=False, )
    country_name = serializers.CharField(source='country.name', required=False, )
    parent_name = serializers.CharField(source='parent.name', required=False, )

    class Meta:
        model = Ubigeo
        fields = '__all__'


class UbigeoBasic__Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ubigeo
        fields = ('id', 'code', 'name', 'phone_code',)


class UbigeoBasic_Serializer(serializers.ModelSerializer):
    parent = UbigeoBasic__Serializer(many=False, read_only=True)

    class Meta:
        model = Ubigeo
        fields = ('id', 'code', 'name', 'phone_code', 'parent',)


class UbigeoBasicSerializer(serializers.ModelSerializer):
    parent = UbigeoBasic_Serializer(many=False, read_only=True)
    country = CountryBasicSerializer(many=False, read_only=True)
    ubigeo_type = UbigeoTypeBasicSerializer(many=False, read_only=True)

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.name
        if obj.parent_id:
            parent_name = obj.parent.name
            name = "%s / %s" % (parent_name, obj.name)
            if obj.parent.parent_id:
                parent_parent_name = obj.parent.parent.name
                name = "%s / %s / %s" % (parent_parent_name, parent_name, obj.name)
        return name

    class Meta:
        model = Ubigeo
        fields = ('id', 'code', 'name', 'phone_code', 'parent',
                  'country', 'ubigeo_type',)


class UbigeoListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.name
        if obj.parent_id:
            parent_name = obj.parent.name
            name = "%s / %s" % (parent_name, obj.name)
            if obj.parent.parent_id:
                parent_parent_name = obj.parent.parent.name
                name = "%s / %s / %s" % (parent_parent_name, parent_name, obj.name)
        return name

    class Meta:
        model = Ubigeo
        fields = ('id', 'name')
