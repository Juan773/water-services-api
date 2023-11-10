import datetime
import decimal
import json
import re

from django.db.models import Q, Value
from django.db.models.functions import Concat, LPad

from water_services_api.apps.core.exceptions import NumberDecimalFormatException, ErrorNumberConvertDecimal
from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Plan import Plan
from water_services_api.apps.operation.models.Quota import Quota, QuotaDetail
from water_services_api.apps.operation.models.Service import Service
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


def get_month_name(month):
    try:
        months = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre']
        return months[month]
    except Exception:
        return ''


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


def get_total_month(client_id, date, month, year):

    quota = Quota.objects.filter(month=month, year=year, is_paid=True).first()
    if quota and quota.id:
        return quota.total
    client = Client.objects.filter(pk=client_id).first()
    plan = Plan.objects.filter(pk=client.plan_id).first()
    services = Service.objects.filter(is_active=True).values_list('id', 'cost', named=True)
    cost_reconnection = 0

    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    month_date = date.month
    year_date = date.year
    day_date = date.day
    year_month_date = int("%s%s" % (year_date, str(month_date).zfill(2)))
    year_month = int("%s%s" % (year, str(month).zfill(2)))

    is_finalized_contract = False
    if client.end_date and client.is_finalized_contract is True:
        date_finalized = datetime.datetime.strptime(client.end_date.strftime("%Y-%m-%d"), '%Y-%m-%d').date()
        year_month_date_finalized = int("%s%s" % (date_finalized.year, str(date_finalized.month).zfill(2)))
        if year_month_date_finalized <= year_month:
            is_finalized_contract = True

    count = 0
    if is_finalized_contract is False:
        # generate months not paid
        quotas_not_paid = Quota.objects.filter(client_id=client_id, is_paid=False)
        if quotas_not_paid.exists():
            count = quotas_not_paid.filter(year_month__lt=year_month_date).count()

        # calculate the cost for reconnection
        if count == plan.reconnection_months:
            if client.is_retired is False and day_date > plan.extension_days:
                cost_reconnection = plan.reconnection_cost
            elif client.is_retired is True and day_date > plan.retired_extension_days:
                cost_reconnection = plan.reconnection_cost
        elif count > plan.reconnection_months:
            cost_reconnection = plan.reconnection_cost

    total = 0
    if is_finalized_contract is False and year_month == year_month_date-1:
        total = total + cost_reconnection

    if client and is_finalized_contract is False:
        if plan.client_type.code == 'socio':
            total = total + plan.cost
        elif plan.client_type.code == 'user':
            total = total + plan.cost

        if count == 1:
            if client.is_retired is False and plan.extension_days < day_date:
                total = total + plan.mora
            elif client.is_retired is True and plan.retired_extension_days < day_date:
                total = total + plan.mora
        elif count > 1:
            total = total + plan.mora
        for detail in services:
            total = total + detail.cost
    elif plan and client:
        total = total + plan.other_expenses

    return total


def update_total_month(client_id, date, month, year):

    quota_paid = Quota.objects.filter(month=month, year=year, is_paid=True).first()
    if quota_paid and quota_paid.id:
        raise Exception('El mes %s-%s ya fue cancelado.' % (month, year))

    quota = Quota.objects.filter(month=month, year=year, is_paid=False).first()
    if not quota:
        raise Exception('El mes %s-%s no ha sido generado.' % (month, year))

    client = Client.objects.filter(pk=client_id).first()
    plan = Plan.objects.filter(pk=client.plan_id).first()
    services = Service.objects.filter(is_active=True).values_list('id', 'cost', 'name', 'order', named=True)
    cost_reconnection = 0

    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    month_date = date.month
    year_date = date.year
    day_date = date.day
    year_month_date = int("%s%s" % (year_date, str(month_date).zfill(2)))
    year_month = int("%s%s" % (year, str(month).zfill(2)))

    is_finalized_contract = False
    if client.end_date and client.is_finalized_contract is True:
        date_finalized = datetime.datetime.strptime(client.end_date.strftime("%Y-%m-%d"), '%Y-%m-%d').date()
        year_month_date_finalized = int("%s%s" % (date_finalized.year, str(date_finalized.month).zfill(2)))
        if year_month_date_finalized <= year_month:
            is_finalized_contract = True

    count = 0
    if is_finalized_contract is False:
        # generate months not paid
        quotas_not_paid = Quota.objects.filter(client_id=client_id, is_paid=False)
        if quotas_not_paid.exists():
            count = quotas_not_paid.filter(year_month__lt=year_month_date).count()

        # calculate the cost for reconnection
        if count == plan.reconnection_months:
            if client.is_retired is False and day_date > plan.extension_days:
                cost_reconnection = plan.reconnection_cost
            elif client.is_retired is True and day_date > plan.retired_extension_days:
                cost_reconnection = plan.reconnection_cost
        elif count > plan.reconnection_months:
            cost_reconnection = plan.reconnection_cost

    total = 0
    cost_reconnection_item = 0
    cost_user_item = 0
    cost_associate_item = 0
    cost_mora = 0
    cost_administrative = 0
    gloss_reconnection = 'Corte/Reconexion'
    gloss_cost_user = 'Cuota:Contrapest. por servicio agua-Usuarios'
    gloss_cost_associate = 'Cuota:Contrapest. por servicio agua-Socios'
    gloss_mora = 'Mora'
    gloss_administration = 'Gastos administrativos'
    list_add = []
    list_update = []

    details = QuotaDetail.objects.filter(quota__client_id=client_id, quota__month=month, quota__year=year)

    if is_finalized_contract is False and year_month == year_month_date-1:
        cost_reconnection_item = cost_reconnection
    total = total + cost_reconnection_item

    if client and is_finalized_contract is False:
        if plan.client_type.code == 'socio':
            cost_associate_item = plan.cost
        elif plan.client_type.code == 'user':
            cost_user_item = plan.cost
        total = total + cost_associate_item + cost_user_item

        if count == 1:
            if client.is_retired is False and plan.extension_days < day_date:
                cost_mora = plan.mora
            elif client.is_retired is True and plan.retired_extension_days < day_date:
                cost_mora = plan.mora
        elif count > 1:
            cost_mora = plan.mora
        total = total + cost_mora

        for detail in services:
            cost_service = 0
            if is_finalized_contract is False:
                cost_service = detail.cost
            total = total + cost_service
    elif plan and client:
        cost_administrative = plan.other_expenses
        total = total + cost_administrative

    for detail in services:
        qd = details.filter(quota_id=quota.id, service_id=detail.id).first()
        if qd:
            qd.gloss = detail.name
            qd.cost = detail.cost
            qd.amount = detail.cost
            qd.order = detail.order
            list_update.append(qd)
        else:
            data_quota_detail = QuotaDetail(
                quota_id=quota.id,
                service_id=detail.id,
                gloss=detail.name,
                quantity=1,
                cost=detail.cost,
                amount=detail.cost,
                order=detail.order
            )
            list_add.append(data_quota_detail)
    qd = details.filter(quota_id=quota.id, gloss=gloss_cost_associate).first()

    if qd:
        qd.cost = cost_associate_item
        qd.amount = cost_associate_item
        list_update.append(qd)
    else:
        data_quota_detail = QuotaDetail(
            quota_id=quota.id,
            service_id=None,
            gloss=gloss_cost_associate,
            quantity=1,
            cost=cost_associate_item,
            amount=cost_associate_item,
            order=2
        )
        list_add.append(data_quota_detail)

    qd = details.filter(quota_id=quota.id, gloss=gloss_cost_user).first()
    if qd:
        qd.cost = cost_user_item
        qd.amount = cost_user_item
        list_update.append(qd)
    else:
        data_quota_detail = QuotaDetail(
            quota_id=quota.id,
            service_id=None,
            gloss=gloss_cost_user,
            quantity=1,
            cost=cost_user_item,
            amount=cost_user_item,
            order=3
        )
        list_add.append(data_quota_detail)

    qd = details.filter(quota_id=quota.id, gloss=gloss_mora).first()
    if qd:
        qd.cost = cost_mora
        qd.amount = cost_mora
        list_update.append(qd)
    else:
        data_quota_detail = QuotaDetail(
            quota_id=quota.id,
            service_id=None,
            gloss=gloss_mora,
            quantity=1,
            cost=cost_mora,
            amount=cost_mora,
            order=6
        )
        list_add.append(data_quota_detail)

    qd = details.filter(quota_id=quota.id, gloss=gloss_reconnection).first()
    if qd:
        qd.cost = cost_reconnection_item
        qd.amount = cost_reconnection_item
        list_update.append(qd)
    else:
        data_quota_detail = QuotaDetail(
            quota_id=quota.id,
            service_id=None,
            gloss=gloss_reconnection,
            quantity=1,
            cost=cost_reconnection_item,
            amount=cost_reconnection_item,
            order=5
        )
        list_add.append(data_quota_detail)

    qd = details.filter(quota_id=quota.id, gloss=gloss_administration).first()
    if qd:
        qd.cost = cost_administrative
        qd.amount = cost_administrative
        list_update.append(qd)
    else:
        data_quota_detail = QuotaDetail(
            quota_id=quota.id,
            service_id=None,
            gloss=gloss_administration,
            quantity=1,
            cost=cost_administrative,
            amount=cost_administrative,
            order=8
        )
        list_add.append(data_quota_detail)

    quota.total = total
    quota.save()
    QuotaDetail.objects.bulk_update(list_update, ["gloss", "cost", "amount"])
    QuotaDetail.objects.bulk_create(list_add)

    return total
