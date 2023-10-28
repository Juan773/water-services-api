from water_services_api.apps.core.base import BasePermission


class UserPermissions(BasePermission):
    perms_map = {
        'add': 'auth.add_user',
        'edit': 'auth.view_user',
        'update': 'auth.update_user',
        'delete': 'auth.delete_user',
        'change_password': 'auth.change_password_user',
        'view_groups': 'auth.view_group_user',
        'change_group': 'auth.change_group_user',
        'view_permissions': 'auth.view_permission_user',
        'change_permission': 'auth.change_permission_user'
    }

    permission_from_user = None
