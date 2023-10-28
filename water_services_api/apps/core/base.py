import re


class BasePermission(object):
    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True
        else:
            elements = re.findall(r'\w+', str(request.path))
            url_path = elements[len(elements) - 1]
            if url_path in self.perms_map:
                self.permission_from_user = self.perms_map[url_path]

            perms = (self.permission_from_user,
                     )
            if request.user.has_perms(perms):
                return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True
        else:
            elements = re.findall(r'\w+', str(request.path))
            url_path = elements[len(elements) - 1]
            if url_path in self.perms_map:
                self.permission_from_user = self.perms_map[url_path]

            perms = (self.permission_from_user,
                     )

            if request.user.has_perms(perms):
                return True
