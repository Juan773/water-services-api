from water_services_api.apps.core.base import BasePermission


class DocumentTypePermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_documenttype',
        'edit': 'configuration.view_documenttype',
        'update': 'configuration.update_documenttype',
        'delete': 'configuration.delete_documenttype'
    }

    permission_from_user = None
