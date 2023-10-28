from rest_framework import serializers

from water_services_api.apps.configuration.serializers.Person import PersonBasicSerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    person = PersonBasicSerializer()
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    def get_groups(self, obj):
        return obj.groups.count()

    def get_entities(self, obj):
        return obj.entities.count()

    def get_permissions(self, obj):
        return len(obj.get_all_permissions())

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password', 'first_name', 'last_name', 'last_login', 'user_permissions',
                   'password_change_at', 'date_new_change_at',)
