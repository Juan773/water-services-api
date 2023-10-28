from water_services_api.apps.core.base import BasePermission


class GroupPermissions(BasePermission):
    perms_map = {
        'add': 'auth.add_group',
        'edit': 'auth.view_group',
        'update': 'auth.change_group',
        'delete': 'auth.delete_group',
        'change_permission': 'auth.change_permission_group',
        'view_permissions': 'auth.view_permission_group'
    }

    permission_from_user = None
