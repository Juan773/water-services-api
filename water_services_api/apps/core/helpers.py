import decimal
import json
import re

from django.db.models import Q

from water_services_api.apps.core.exceptions import NumberDecimalFormatException, ErrorNumberConvertDecimal
from water_services_api.settings import IS_PRODUCTION


def parse_error(message):
    error = {
        "message": message if not IS_PRODUCTION else 'Ocurrió un error en el servidor',
        "status": False
    }
    return error


def parse_success(data, message=""):
    error = {
        "data": data,
        "message": message,
        "status": True
    }
    return error


def parse_error_custom(status, data, message=""):
    error = {
        "data": data,
        "message": message,
        "status": status
    }
    return error


def validate_param(param, data):
    result = None
    if param in data:
        if type(data[param]) is str:
            if (data[param].strip() != '') and (data[param] != 'null'):
                result = data[param].strip()
        else:
            if data[param] is not None:
                result = data[param]
    return result


def str_to_array(data):
    try:
        if type(data) == str:
            return json.loads(data)
        else:
            return data
    except Exception:
        return []


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    if len(terms) == 0:
        terms = ['']
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def convert_to_decimal(data, format_=None):
    try:
        _format = "%0.2f"
        if format_ is not None:
            _format = format_
        number = decimal.Decimal(_format % decimal.Decimal(data))
        context = decimal.getcontext()
        context.rounding = decimal.ROUND_HALF_UP
        return round(decimal.Decimal(number), 2)
    except Exception as e:
        raise NumberDecimalFormatException(str(e))


def convert_to_decimal_to_four(data):
    try:
        return decimal.Decimal("%0.4f" % decimal.Decimal(data))
    except Exception:
        raise ErrorNumberConvertDecimal()


def convert_to_decimal_to_two(data):
    try:
        return decimal.Decimal("%0.2f" % decimal.Decimal(data))
    except Exception:
        raise ErrorNumberConvertDecimal()


def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "True", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true", "t", "1"): return True
    if str(value).lower() in ("no", "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

