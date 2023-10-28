from water_services_api.apps.core.base import BasePermission


class CountryPermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_country',
        'edit': 'configuration.view_country',
        'update': 'configuration.update_country',
        'delete': 'configuration.delete_country'
    }

    permission_from_user = None
