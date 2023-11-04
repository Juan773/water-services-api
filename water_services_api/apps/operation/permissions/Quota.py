from water_services_api.apps.core.base import BasePermission


class QuotaPermissions(BasePermission):
    perms_map = {
        'add': 'operation.add_quota',
        'edit': 'operation.view_quota',
        'update': 'operation.update_quota',
        'delete': 'operation.delete_quota'
    }

    permission_from_user = None
