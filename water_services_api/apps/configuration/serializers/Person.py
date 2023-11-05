from rest_framework import serializers

from water_services_api.apps.configuration.models.Person import Person
from water_services_api.apps.configuration.serializers.Country import CountryBasicSerializer
from water_services_api.apps.core.HostValues import HostValues


class PersonSerializer(serializers.ModelSerializer):
    country = CountryBasicSerializer(many=False, read_only=True)

    class Meta:
        model = Person
        # fields = '__all__'
        exclude = ('created_at', 'updated_at',)


class PersonBasicSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_logo(self, q):
        foto = ""
        request = self.context.get('request')
        if request:
            dominio = HostValues.domain(request)
            if q.logo:
                foto = dominio + q.logo.url
            else:
                foto = ""
        return foto

    def get_thumbnail(self, q):
        foto = ""
        request = self.context.get('request')
        if request:
            dominio = HostValues.domain(request)
            if q.logo:
                if q.thumbnail:
                    foto = dominio + q.thumbnail.url
                else:
                    foto = ""
            else:
                foto = ""
        return foto

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'full_name', 'thumbnail', 'logo')
    # exclude = ('created_at','updated_at',)


class PersonBasicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'full_name',)


class PersonEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'full_name',)


class PersonLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'logo', 'thumbnail',)


class PersonInfoSerializer(serializers.ModelSerializer):
    country = CountryBasicSerializer(many=False, read_only=True)

    class Meta:
        model = Person
        fields = ('id', 'logo', 'thumbnail', 'full_name', 'country')
    # exclude = ('created_at','updated_at',)


class PersonSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'full_name', 'thumbnail',)
