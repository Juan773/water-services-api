from django.urls import re_path, include
from rest_framework import routers

# from water_services_api.apps.configuration.views.PersonView import PersonSearchViewSet, PersonViewSet
from water_services_api.apps.configuration.views.CountryView import CountryViewSet
from water_services_api.apps.configuration.views.PersonView import PersonViewSet
from water_services_api.apps.configuration.views.UbigeoTypeView import UbigeoTypeViewSet
from water_services_api.apps.configuration.views.UbigeoView import UbigeoViewSet

router = routers.DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'ubigeo_type', UbigeoTypeViewSet)
router.register(r'ubigeos', UbigeoViewSet)
router.register(r'person', PersonViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
