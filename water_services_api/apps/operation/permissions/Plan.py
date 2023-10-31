from water_services_api.apps.core.base import BasePermission


class PlanPermissions(BasePermission):
    perms_map = {
        'add': 'operation.add_plan',
        'edit': 'operation.view_plan',
        'update': 'operation.update_plan',
        'delete': 'operation.delete_plan'
    }

    permission_from_user = None
