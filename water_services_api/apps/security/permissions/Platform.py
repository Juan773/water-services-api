from water_services_api.apps.core.base import BasePermission


class PlatformPermissions(BasePermission):
    perms_map = {
        'add': 'security.add_platform',
        'edit': 'security.view_platform',
        'update': 'security.change_platform',
        'delete': 'security.delete_platform',
    }

    permission_from_user = None
