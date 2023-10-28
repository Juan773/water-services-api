from water_services_api.apps.core.base import BasePermission


class ModulePermissions(BasePermission):
    perms_map = {
        'add': 'security.add_module',
        'edit': 'security.view_module',
        'update': 'security.update_module',
        'delete': 'security.delete_module', }

    permission_from_user = None
