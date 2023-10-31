from water_services_api.apps.core.base import BasePermission


class SituationPermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_situation',
        'edit': 'configuration.view_situation',
        'update': 'configuration.update_situation',
        'delete': 'configuration.delete_situation'
    }

    permission_from_user = None
