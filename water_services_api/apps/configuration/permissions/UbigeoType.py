from water_services_api.apps.core.base import BasePermission


class UbigeoTypePermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_ubigeotype',
        'edit': 'configuration.view_ubigeotype',
        'update': 'configuration.update_ubigeotype',
        'delete': 'configuration.delete_ubigeotype'
    }

    permission_from_user = None
