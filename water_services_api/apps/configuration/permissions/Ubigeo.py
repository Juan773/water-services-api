from water_services_api.apps.core.base import BasePermission


class UbigeoPermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_ubigeo',
        'edit': 'configuration.view_ubigeo',
        'update': 'configuration.update_ubigeo',
        'delete': 'configuration.delete_ubigeo', }

    permission_from_user = None
