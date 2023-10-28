from rest_framework import permissions


class PermDisaryList(permissions.DjangoObjectPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }
