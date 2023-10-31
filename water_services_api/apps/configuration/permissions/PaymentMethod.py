from water_services_api.apps.core.base import BasePermission


class PaymentMethodPermissions(BasePermission):
    perms_map = {
        'add': 'configuration.add_paymentmethod',
        'edit': 'configuration.view_paymentmethod',
        'update': 'configuration.update_paymentmethod',
        'delete': 'configuration.delete_paymentmethod'
    }

    permission_from_user = None
