from water_services_api.apps.core.base import BasePermission


class PaymentPermissions(BasePermission):
    perms_map = {
        'add': 'operation.add_payment',
        'edit': 'operation.view_payment',
        'update': 'operation.update_payment',
        'delete': 'operation.delete_payment'
    }

    permission_from_user = None
