from water_services_api.apps.core.base import BasePermission


class ClientPermissions(BasePermission):
    perms_map = {
        'add': 'operation.add_client',
        'edit': 'operation.view_client',
        'update': 'operation.update_client',
        'delete': 'operation.delete_client'
    }

    permission_from_user = None
