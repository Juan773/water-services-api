import calendar
import datetime

from dateutil import relativedelta
from django.db import transaction
from django.db.models import Value, Min
from django.db.models.functions import LPad, Concat
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from oauth2_provider.models import  get_access_token_model, get_refresh_token_model

from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Plan import Plan
from water_services_api.apps.operation.models.Quota import Quota
from water_services_api.apps.operation.models.Service import Service

AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()


class FunctionsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[],
            url_path='generate_quota', url_name='generate_quota')
    def generate_quota(self, request, format=None):
        try:
            with transaction.atomic():
                client_id = request.data['client_id']
                client = Client.objects.filter(pk=client_id).first()

                if client:
                    if not client.plan_id:
                        result = dict(
                            estado=False,
                            mensaje='La persona no tiene un plan asignado.'
                        )
                        result = parse_success(result)
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
                else:
                    result = dict(
                        estado=False,
                        mensaje='El cliente no existe.'
                    )
                    result = parse_success(result)
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

                date = datetime.datetime.now().date()
                month = date.month
                year = date.year
                day = date.day
                year_month = int("%s%s" % (year, LPad(month, 2, Value('0'))))

                plan = Plan.objects.filter(pk=client.plan_id).first()

                max_year_month = int("%s%s" % (year, 12))
                min_year_month = int("%s%s" % (year, month))
                quotas = Quota.objects.filter(client_id=client_id, is_paid=False)
                if quotas.exists():
                    quotas = quotas.annotate(year_month_quota=Concat('year', LPad('month', 2, Value('0'))))
                    min_quota = quotas.aggregate(Min('year_month_quota'))
                    min_year_month = int(min_quota['year_month_quota__max'])

                max_date = "%s/%s/%s" % (year, month, calendar.monthrange(year, month)[1])
                min_date = "%s/%s/%s" % (str(min_year_month)[0:4], str(min_year_month)[4:], '01')
                # convert string to date object
                start_date = datetime.datetime.strptime(min_date, "%Y/%m/%d")
                end_date = datetime.datetime.strptime(max_date, "%Y/%m/%d")

                # Get the relativedelta between two dates
                delta = relativedelta.relativedelta(end_date, start_date)

                # get months difference
                difference_months = delta.months + (delta.years * 12)

                if difference_months >= 2:
                    # calculate the cost for reconnection
                    if difference_months == plan.reconnection_months:
                        if client.is_retired is False and day > plan.extension_days:
                            cost_reconnection = plan.reconnection_cost
                        elif client.is_retired is True and day > plan.retired_extension_days:
                            cost_reconnection = plan.reconnection_cost
                    elif difference_months > plan.reconnection_months:
                        cost_reconnection = plan.reconnection_cost

                services = Service.objects.filter(is_active=True)

                for month_item in range(1, 12):
                    total = 0
                    is_finalized_contract = False
                    if client.date_finalized_contract and client.is_finalized_contract is True:
                        date_finalized = datetime.datetime.strptime(client.date_finalized_contract, '%Y-%m-%d').date()
                        if date_finalized.month <= month_item:
                            is_finalized_contract = True

                    if is_finalized_contract is True and month_item == month - 1:
                        total = total + cost_reconnection

                    if client and is_finalized_contract is False:
                        if plan.client_type.code == 'socio':
                            total = total + plan.cost
                        elif plan.client_type.code == 'user':
                            total = total + plan.cost

                        if client.is_retired is False and plan.extension_days < day:
                            total = total + plan.reconnection_cost
                        elif client.is_retired is True and plan.retired_extension_days < day:
                            total = total + plan.reconnection_cost

                        for detail in services:
                            total = total + detail.cost
                    elif plan:
                        total = total + plan.other_expenses

                result = parse_success(
                    [],
                    "Se agregó correctamente",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

