from django.urls import re_path, include
from rest_framework import routers

from water_services_api.apps.operation.views.ClientView import ClientViewSet
from water_services_api.apps.operation.views.FunctionsView import FunctionsViewSet
from water_services_api.apps.operation.views.PaymentView import PaymentViewSet
from water_services_api.apps.operation.views.PlanView import PlanViewSet
from water_services_api.apps.operation.views.QuotaView import QuotaViewSet
from water_services_api.apps.operation.views.ServiceView import ServiceViewSet

router = routers.DefaultRouter()
router.register(r'client', ClientViewSet)
router.register(r'payment', PaymentViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'service', ServiceViewSet)
router.register(r'quota', QuotaViewSet)
router.register(r'functions', FunctionsViewSet, basename='functions')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
