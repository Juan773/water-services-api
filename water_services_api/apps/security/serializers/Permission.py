from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    # persona_direcciones = DireccionBasicSerializer(many=True, read_only=True)
    app_label = serializers.ReadOnlyField(source='content_type.app_label')
    model = serializers.ReadOnlyField(source='content_type.model')
    content_type_name = serializers.ReadOnlyField(source='content_type.name')
    permission = serializers.SerializerMethodField()

    def get_permission(self, perm):
        return "%s.%s.%s" % (perm.content_type.app_label, perm.content_type.model, perm.codename.split('_')[0])

    class Meta:
        model = Permission
        fields = '__all__'


class PermissionEditSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    content_type_id = serializers.ReadOnlyField(source='content_type.id')

    def get_content_type(self, p):
        return {
            'id': p.content_type.id,
            'app_label': p.content_type.app_label,
            'model': p.content_type.model,
        }

    class Meta:
        model = Permission
        fields = '__all__'


class PermissionBasicSerializer(serializers.ModelSerializer):
    # # persona_direcciones = DireccionBasicSerializer(many=True, read_only=True)
    app_label = serializers.ReadOnlyField(source='content_type.app_label', required=False, )
    model = serializers.ReadOnlyField(source='content_type.model', required=False, )

    class Meta:
        model = Permission
        fields = '__all__'
