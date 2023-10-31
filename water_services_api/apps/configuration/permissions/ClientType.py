from water_services_api.apps.core.base import BasePermission


class ClientTypePermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_clienttype',
        'edit': 'configuration.view_clienttype',
        'update': 'configuration.update_clienttype',
        'delete': 'configuration.delete_clienttype'
    }

    permission_from_user = None
