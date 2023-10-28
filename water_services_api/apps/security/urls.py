from django.urls import re_path, include
from rest_framework import routers

from water_services_api.apps.security.views.ContentTypeView import ContentTypeViewSet
from water_services_api.apps.security.views.FunctionsView import FunctionsViewSet
from water_services_api.apps.security.views.GroupView import GroupViewSet
from water_services_api.apps.security.views.ModuleView import ModuleViewSet
from water_services_api.apps.security.views.PermissionView import PermissionViewSet
from water_services_api.apps.security.views.PlatformView import PlatformViewSet
from water_services_api.apps.security.views.TokenView import TokenViewSet
from water_services_api.apps.security.views.UserView import UserViewSet

router = routers.DefaultRouter()
router.register(r'token', TokenViewSet, basename='token')
router.register(r'functions', FunctionsViewSet, basename='functions')
router.register(r'content_types', ContentTypeViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'roles', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'platform', PlatformViewSet)
router.register(r'modules', ModuleViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
