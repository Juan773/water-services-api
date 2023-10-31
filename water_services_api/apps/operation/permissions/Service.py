from water_services_api.apps.core.base import BasePermission


class ServicePermissions(BasePermission):
    perms_map = {
        'add': 'operation.add_service',
        'edit': 'operation.view_service',
        'update': 'operation.update_service',
        'delete': 'operation.delete_service'
    }

    permission_from_user = None
