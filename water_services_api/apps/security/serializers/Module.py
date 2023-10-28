from rest_framework import serializers

from water_services_api.apps.security.consonants import MODULES_TYPE
from water_services_api.apps.security.models.Module import Module
from water_services_api.apps.security.serializers.Permission import PermissionBasicSerializer


class ModuleBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name', 'code', 'plural_name',)


class ModuleEditSerializer(serializers.ModelSerializer):
    permission = PermissionBasicSerializer(many=False, read_only=True)
    parent = ModuleBasicSerializer(many=False, read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'platform_id', 'code', 'name', 'plural_name', 'route', 'icon', 'parent',
                  'order', 'level', 'type', 'permission',)


class ModuleSerializer(serializers.ModelSerializer):
    permission_codename = serializers.CharField(source='permission.codename', required=False)
    parent_name = serializers.CharField(source='parent.name', required=False)

    class Meta:
        model = Module
        fields = '__all__'


class ModuleAngularSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('_name')
    icon = serializers.SerializerMethodField('_icon')
    state = serializers.SerializerMethodField('_state')
    route = serializers.SerializerMethodField('_route')

    def _name(self, obj):
        return obj.plural_name

    def _icon(self, obj):
        return obj.icon

    def _state(self, obj):
        return obj.estado_router

    def _route(self, obj):
        return obj.route

    class Meta:
        model = Module
        fields = ('id', 'code', 'name', 'icon', 'state', 'route',)


class ModuleAngular10Serializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('_title')
    icon = serializers.SerializerMethodField('_icon')
    routerLink = serializers.SerializerMethodField('routerLink_')
    parentId = serializers.SerializerMethodField('parentId_')

    def _title(self, obj):
        return obj.plural_name

    def _icon(self, obj):
        return obj.icon

    def routerLink_(self, obj):
        return obj.route

    def parentId_(self, obj):
        if obj.parent_id:
            return obj.parent_id
        else:
            return 0

    class Meta:
        model = Module
        fields = ('id', 'title', 'icon', 'routerLink', 'parentId',)


class ModuleChildrenSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="name")
    link = serializers.ReadOnlyField(source="route")
    type = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_id(self, m):
        return str(m.id)

    def get_type(self, m):
        return MODULES_TYPE[m.type]

    def get_fields(self):
        fields = super(ModuleChildrenSerializer, self).get_fields()
        fields['children'] = ModuleChildrenSerializer(many=True)
        return fields

    class Meta:
        model = Module
        fields = ('id', 'title', 'type', 'icon', 'link', 'children',)


class ModuleCustomSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_id(self, m):
        return str(m.id)

    def get_title(self, m):
        return m.plural_title

    class Meta:
        model = Module
        fields = (
            'id', 'title', 'icon', 'expanded', 'group', 'hidden', 'home', 'link', 'url', 'target', 'order',)
