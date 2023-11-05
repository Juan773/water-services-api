import calendar
import datetime

from dateutil import relativedelta
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from oauth2_provider.models import get_access_token_model, get_refresh_token_model

from water_services_api.apps.core.helpers import parse_success, parse_error
from water_services_api.apps.operation.models.Client import Client
from water_services_api.apps.operation.models.Plan import Plan
from water_services_api.apps.operation.models.Quota import Quota, QuotaDetail
from water_services_api.apps.operation.models.Service import Service

AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()


class FunctionsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated, ],
            url_path='generate_quota', url_name='generate_quota')
    def generate_quota(self, request, format=None):
        try:
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

            # min_month = month
            # min_year = year
            max_month = 12
            max_year = year
            client_date_start = datetime.datetime.strptime(client.start_date.strftime("%Y/%m/%d"), "%Y/%m/%d"). \
                date()
            client_year_month = int("%s%s" % (client_date_start.year, str(client_date_start.month).zfill(2)))
            quotas = Quota.objects.filter(client_id=client_id, year_month__gte=client_year_month)
            if quotas.exists():
                quota_not_paid = quotas.filter(is_paid=False)
                if quota_not_paid.exists():
                    min_quota = quota_not_paid.order_by('year_month')[0]
                    min_month = min_quota.month
                    min_year = min_quota.year
                else:
                    min_quota = quotas.order_by('year_month')[0]
                    min_month = min_quota.month
                    min_year = min_quota.year
            else:
                min_month = client_date_start.month
                min_year = client_date_start.year

            max_date_old = "%s/%s/%s" % (year, month, 1)
            min_date_old = "%s/%s/%s" % (min_year, min_month, 1)
            # convert string to date object
            start_date_old = datetime.datetime.strptime(min_date_old, "%Y/%m/%d")
            end_date_old = datetime.datetime.strptime(max_date_old, "%Y/%m/%d")
            # Get the relativedelta between two dates
            delta = relativedelta.relativedelta(end_date_old, start_date_old)
            # get months difference
            diff_months_old = delta.months + (delta.years * 12)

            plan = Plan.objects.filter(pk=client.plan_id).first()
            cost_reconnection = 0
            if diff_months_old >= 2:
                # calculate the cost for reconnection
                if diff_months_old == plan.reconnection_months:
                    if client.is_retired is False and day > plan.extension_days:
                        cost_reconnection = plan.reconnection_cost
                    elif client.is_retired is True and day > plan.retired_extension_days:
                        cost_reconnection = plan.reconnection_cost
                elif diff_months_old > plan.reconnection_months:
                    cost_reconnection = plan.reconnection_cost

            services = Service.objects.filter(is_active=True).iterator()

            max_date = "%s/%s/%s" % (max_year, max_month, 1)
            min_date = "%s/%s/%s" % (min_year, min_month, 1)
            # convert string to date object
            start_date = datetime.datetime.strptime(min_date, "%Y/%m/%d")
            end_date = datetime.datetime.strptime(max_date, "%Y/%m/%d")
            # Get the relativedelta between two dates
            delta = relativedelta.relativedelta(end_date, start_date)
            # get months difference
            diff_months = delta.months + (delta.years * 12)

            gloss_reconnection = 'Corte/Reconexion'
            gloss_cost_user = 'Cuota:Contrapest. por servicio agua-Usuarios'
            gloss_cost_associate = 'Cuota:Contrapest. por servicio agua-Socios'
            gloss_mora = 'Mora'
            gloss_administration = 'Gastos administrativos'

            diff_months = diff_months + 1

            details = QuotaDetail.objects.filter(quota__client_id=client_id, quota__year_month__gte=client_year_month)

            list_update_q = []
            list_add = []
            list_update = []
            with transaction.atomic():
                for item in range(0, diff_months):
                    if item == 0:
                        date_item = start_date.date()
                    else:
                        date_item = start_date.date() + relativedelta.relativedelta(months=+item)
                    month_item = date_item.month
                    year_item = date_item.year

                    max_date_item = "%s/%s/%s" % (year, month, 1)
                    min_date_item = "%s/%s/%s" % (year_item, month_item, 1)
                    # convert string to date object
                    start_date_item = datetime.datetime.strptime(min_date_item, "%Y/%m/%d")
                    end_date_item = datetime.datetime.strptime(max_date_item, "%Y/%m/%d")
                    # Get the relativedelta between two dates
                    delta = relativedelta.relativedelta(end_date_item, start_date_item)
                    # get months difference
                    diff_months_item = delta.months + (delta.years * 12)

                    total = 0
                    cost_reconnection_item = 0
                    cost_user_item = 0
                    cost_associate_item = 0
                    cost_mora = 0
                    cost_administrative = 0

                    is_finalized_contract = False
                    if client.end_date and client.is_finalized_contract is True:
                        date_finalized = datetime.datetime.strptime(client.end_date, '%Y-%m-%d').date()
                        if date_finalized.month <= month_item:
                            is_finalized_contract = True

                    if is_finalized_contract is False and month_item == month - 1:
                        cost_reconnection_item = cost_reconnection
                    total = total + cost_reconnection_item

                    if client and is_finalized_contract is False:
                        if plan.client_type.code == 'socio':
                            cost_associate_item = plan.cost
                        elif plan.client_type.code == 'user':
                            cost_user_item = plan.cost
                        total = total + cost_associate_item + cost_user_item

                        if diff_months_item == 1:
                            if client.is_retired is False and plan.extension_days < day:
                                cost_mora = plan.reconnection_cost
                            elif client.is_retired is True and plan.retired_extension_days < day:
                                cost_mora = plan.reconnection_cost
                        elif diff_months_item > 1:
                            cost_mora = plan.reconnection_cost
                        total = total + cost_mora
                    elif plan:
                        cost_administrative = plan.other_expenses
                        total = total + cost_administrative

                    q = quotas.filter(month=month_item, year=year_item, is_paid=False).\
                        first()

                    for detail in services:
                        cost_service = 0
                        if is_finalized_contract is False:
                            cost_service = detail.cost
                        total = total + cost_service

                        if q:
                            qd = details.filter(quota_id=q.id, service_id=detail.id).first()
                            if qd:
                                qd.gloss = detail.name
                                qd.cost = detail.cost
                                qd.amount = detail.cost
                                list_update.append(qd)
                            else:
                                data_quota_detail = QuotaDetail(
                                    quota_id=q.id,
                                    service_id=detail.id,
                                    gloss=detail.name,
                                    quantity=1,
                                    cost=detail.cost,
                                    amount=detail.cost,
                                    order=detail.order
                                )
                                list_add.append(data_quota_detail)
                        else:
                            data_quota_detail = QuotaDetail(
                                quota_id=q.id,
                                service_id=detail.id,
                                gloss=detail.name,
                                quantity=1,
                                cost=detail.cost,
                                amount=detail.cost,
                                order=detail.order
                            )
                            list_add.append(data_quota_detail)

                    if not q:
                        data_quota = dict(
                            client_id=client_id,
                            plan_id=client.plan_id,
                            month=month_item,
                            year=year_item,
                            year_month=int("%s%s" % (year_item, str(month_item).zfill(2))),
                            total=total,
                            is_paid=False
                        )
                        q = Quota.objects.create(**data_quota)
                    else:
                        q.total = total
                        list_update_q.append(q)

                    qd = details.filter(quota_id=q.id, gloss=gloss_cost_associate).first()

                    if qd:
                        qd.cost = cost_associate_item
                        qd.amount = cost_associate_item
                        list_update.append(qd)
                    else:
                        data_quota_detail = QuotaDetail(
                                quota_id=q.id,
                                service_id=None,
                                gloss=gloss_cost_associate,
                                quantity=1,
                                cost=cost_associate_item,
                                amount=cost_associate_item,
                                order=2
                             )
                        list_add.append(data_quota_detail)
                        # QuotaDetail.objects.create(**data_quota_detail)
                    qd = details.filter(quota_id=q.id, gloss=gloss_cost_user).first()
                    if qd:
                        qd.cost = cost_user_item
                        qd.amount = cost_user_item
                        list_update.append(qd)
                    else:
                        data_quota_detail = QuotaDetail(
                            quota_id=q.id,
                            service_id=None,
                            gloss=gloss_cost_user,
                            quantity=1,
                            cost=cost_user_item,
                            amount=cost_user_item,
                            order=3
                        )
                        list_add.append(data_quota_detail)
                        # QuotaDetail.objects.create(**data_quota_detail)
                    qd = details.filter(quota_id=q.id, gloss=gloss_mora).first()
                    if qd:
                        qd.cost = cost_mora
                        qd.amount = cost_mora
                        list_update.append(qd)
                    else:
                        data_quota_detail = QuotaDetail(
                            quota_id=q.id,
                            service_id=None,
                            gloss=gloss_mora,
                            quantity=1,
                            cost=cost_mora,
                            amount=cost_mora,
                            order=6
                        )
                        list_add.append(data_quota_detail)
                        # QuotaDetail.objects.create(**data_quota_detail)
                    qd = details.filter(quota_id=q.id, gloss=gloss_reconnection).first()
                    if qd:
                        qd.cost = cost_reconnection_item
                        qd.amount = cost_reconnection_item
                        list_update.append(qd)
                    else:
                        data_quota_detail = QuotaDetail(
                            quota_id=q.id,
                            service_id=None,
                            gloss=gloss_reconnection,
                            quantity=1,
                            cost=cost_reconnection_item,
                            amount=cost_reconnection_item,
                            order=5
                        )
                        list_add.append(data_quota_detail)
                        # QuotaDetail.objects.create(**data_quota_detail)
                    qd = details.filter(quota_id=q.id, gloss=gloss_administration).first()
                    if qd:
                        qd.cost = cost_administrative
                        qd.amount = cost_administrative
                        list_update.append(qd)
                    else:
                        data_quota_detail = QuotaDetail(
                            quota_id=q.id,
                            service_id=None,
                            gloss=gloss_administration,
                            quantity=1,
                            cost=cost_administrative,
                            amount=cost_administrative,
                            order=8
                        )
                        list_add.append(data_quota_detail)

                Quota.objects.bulk_update(list_update_q, ["total"])
                QuotaDetail.objects.bulk_create(list_add)
                QuotaDetail.objects.bulk_update(list_update, ["gloss", "cost", "amount"])

                # for key in list_update:
                #     QuotaDetail.objects.filter(id=key).update(gloss=list_update[key]['gloss'],
                #                                               cost=list_update[key]['cost'],
                #                                               amount=list_update[key]['amount'])

                result = parse_success(
                    '',
                    "Se agregó correctamente",
                )
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error = parse_error(str(e))
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

