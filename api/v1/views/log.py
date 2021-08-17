from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.v1.serializers.log import LogSerializer
from common.paginator import DefaultListPaginator
from openapi.utils import extend_schema
from .base import BaseTenantViewSet
from inventory.models import Permission
from rest_framework import viewsets
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication


@extend_schema(
    roles=['tenant admin', 'global admin'],
    tags = ['log']
)
class UserLogViewSet(BaseTenantViewSet, viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = LogSerializer
    pagination_class = DefaultListPaginator

    def list(self, request, parent_lookup_tenant):
        result = {
            "count":4,
            "next":None,
            "previous":None,
            "results":[
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba85144b",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "login"
                },
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba85144b",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "logout"
                },
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba85144a",
                     "timestamp":"2021-08-17 19:19:12",
                    "action": "login"
                },
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba85144a",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "logout"
                }
            ]
        }
        return Response(result)


@extend_schema(
    roles=['tenant admin', 'global admin'],
    tags = ['log']
)
class AdminLogViewSet(BaseTenantViewSet, viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = LogSerializer
    pagination_class = DefaultListPaginator

    def list(self, request, parent_lookup_tenant):
        result = {
            "count":2,
            "next":None,
            "previous":None,
            "results":[
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba851432",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "add user weichen"
                },
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba851432",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "delete user weichen"
                }
            ]
        }
        return Response(result)
