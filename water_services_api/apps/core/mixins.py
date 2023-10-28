from django_filters import rest_framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime

from water_services_api.apps.core.Permission import PermDisaryList


class DefaultViewSetMixin(object):
    # authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, PermDisaryList)
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)


class SearchViewSetMixin(object):
    # authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)


class TokenViewSetMixin(object):
    """Default settings for view authentication, permissions,
    filtering and pagination."""

    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class ModelViewSet(viewsets.ModelViewSet):
    module_access = None

    # override method DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = datetime.datetime.now()
        instance.save()
        response = {
            "result": "Ok"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
