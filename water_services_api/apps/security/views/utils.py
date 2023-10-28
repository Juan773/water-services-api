from django.contrib.auth.models import Permission
from django.db.models import F

from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.security.models.Module import Module


def get_modules_structure(permissions, is_admin=False):
    result = {}
    try:
        modules = Module.objects.all()

        array_modules = []
        array_submodules = []
        pk_submodules = []
        array_models = []
        for item in modules:
            if item.level == 1 and item.parent_id is None:
                entity = None
                if item.permission_id:
                    entity = item.permission.codename.split('_')[1]
                    array_models.append(entity)

                array_modules.append({
                    'id': item.id,
                    'name': item.plural_title,
                    'model': entity,
                    'actions': {},
                    'children': []
                })

            obj_submodule = None
            # if item.level == 2 and item.parent_id and item.type == 'B':
            if item.level == 2 and item.parent_id:
                entity = None
                if item.permission_id:
                    entity = item.permission.codename.split('_')[1]
                    array_models.append(entity)
                obj_submodule = {
                    'id': item.id,
                    'name': item.plural_title,
                    'model': entity,
                    'parent_id': item.parent_id,
                    'actions': {}
                }

            # if item.level == 3 and item.parent_id and item.type == 'B':
            if item.level == 3 and item.parent_id:
                entity = None
                if item.permission_id:
                    entity = item.permission.codename.split('_')[1]
                    array_models.append(entity)
                obj_submodule = {
                    'id': item.parent_id,
                    'name': item.parent.plural_title,
                    'model': entity,
                    'parent_id': item.parent.parent_id,
                    'actions': {}
                }

            if obj_submodule and obj_submodule['id'] not in pk_submodules:
                array_submodules.append(obj_submodule)
                pk_submodules.append(obj_submodule['id'])

        perms = Permission.objects.filter(content_type__model__in=array_models). \
            values('id', 'name').annotate(model=F('content_type__model'))

        dict_model = {}
        for item in perms:
            key = item['model']
            if key not in dict_model:
                dict_model[key] = []
            obj = item
            obj['status'] = False
            if is_admin:
                obj['status'] = True
            elif obj['id'] in permissions:
                obj['status'] = True
            dict_model[key].append(obj)

        dict_children = {}

        for item in array_submodules:
            if item['model'] and item['model'] in dict_model:
                item['actions'] = dict_model[item['model']]

            key = item['parent_id']
            if key not in dict_children:
                dict_children[key] = []
            dict_children[key].append(item)

        for item in array_modules:
            if item['id'] in dict_children:
                item['children'] = dict_children[item['id']]
            if item['model'] and item['model'] in dict_model:
                item['actions'] = dict_model[item['model']]
        data = array_modules
        result = parse_success(data)

        return result
    except Exception as e:
        result = parse_error(str(e))
    return result
