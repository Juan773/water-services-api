from water_services_api.apps.core.base import BasePermission


class PersonPermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_person',
        'edit': 'configuration.view_person',
        'update': 'configuration.update_person',
        'delete': 'configuration.delete_person'
    }

    permission_from_user = None
