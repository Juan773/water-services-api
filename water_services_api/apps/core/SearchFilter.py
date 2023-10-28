from functools import reduce
from operator import __or__ as OR
from django.db.models import Q
import ast, json


def search_filter(queryset, request):
    limit = request.query_params.get('limit', None)
    q = request.query_params.get('q', None)
    ordering = request.query_params.get('ordering', None)
    f = request.query_params.get('f', None)
    e = request.query_params.get('e', None)

    if e:
        queryset = queryset.exclude(**json.loads(e))

    if f:
        queryset = queryset.filter(**json.loads(f))

    if q:
        queryset = queryset.filter(reduce(OR, [Q(x) for x in ast.literal_eval(q).items()]))

    if ordering:
        queryset = queryset.order_by(*ordering.split(","))

    if limit:
        queryset = queryset[:int(limit)]

    return queryset


# http://localhost:8000/api/comun/paises/searchform/
# ?limit=10&q={"nombre__icontains":"e"}&ordering=nombre,codigo&f={"estado":"0"}

def keys_del(data, keys):
    listado = keys.split(",")
    for p in listado:
        if p in data:
            del data[p]

    return data


def keys_add_none(data, keys):
    listado = keys.split(",")
    data_new = {}
    for p in listado:
        if p in data and data[p] is not None:
            if data[p] == '':
                data_new[p] = None
            else:
                data_new[p] = data[p]
        else:
            data_new[p] = None

    return data_new


def values_concat(data, keys):
    listado = keys.split(",")
    data_new = ''
    for p in listado:
        if p in data and data[p]:
            data_new += " " + data[p]

    return data_new.strip()


def values_obj_add(data, keys, values):
    resul = []
    listado = keys.split(",")
    i = 0
    for p in values.split(","):
        separ = p.split(".")
        if separ[0] in data and data[separ[0]] and data[separ[0]][separ[1]]:
            value = data[separ[0]][separ[1]]
        else:
            value = None
        new = dict(colum=listado[i], value=value)
        i += 1
        resul.append(new)
    return resul


def is_new_in_array(value, array):
    resul = True
    for p in array:
        if p == value:
            resul = False
    return resul


def add_keys_values(data, data_new):
    for p in data_new.keys():
        data[p] = data_new[p]
    return data


def extaer_de_column(listado, key):
    new_lista = []
    for p in listado:
        new_lista.append(p[key])

    return new_lista


def values_all_none(data, keys):
    for p in keys.split(","):
        data[p] = None

    return data


def replace_field(data, field_old, fiel_new):
    if field_old in data:
        data[fiel_new] = data[field_old]
        del data[field_old]

    return data
