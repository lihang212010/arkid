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
                    "uuid":"d34997dd-aec2-4d6e-9ee8-132a20cc2468",
                     "timestamp":"2021-08-17 19:19:12",
                    "action": "login"
                },
                {
                    "uuid":"d34997dd-aec2-4d6e-9ee8-132a20cc2468",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "open app jenkins"
                },
                {
                    "uuid":"d34997dd-aec2-4d6e-9ee8-132a20cc2468",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "open app oauth2"
                },
                {
                    "uuid":"d34997dd-aec2-4d6e-9ee8-132a20cc2468",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "logout"
                },
                {
                    "uuid":"268674b4-32d9-46a7-809b-0a35fc9304cc",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "login"
                },
                {
                    "uuid":"268674b4-32d9-46a7-809b-0a35fc9304cc",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "open app saml-huawei"
                },
                {
                    "uuid":"268674b4-32d9-46a7-809b-0a35fc9304cc",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "open app nodejs"
                },
                {
                    "uuid":"268674b4-32d9-46a7-809b-0a35fc9304cc",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "modify email "
                },
                {
                    "uuid":"268674b4-32d9-46a7-809b-0a35fc9304cc",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "logout"
                },
                {
                    "uuid":"2dd92d66-87bb-4cd4-b4a2-f26fc77fe574",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "login"
                },
                {
                    "uuid":"2dd92d66-87bb-4cd4-b4a2-f26fc77fe574",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "modify mobile-phone"
                },
                {
                    "uuid":"2dd92d66-87bb-4cd4-b4a2-f26fc77fe574",
                     "timestamp":"2021-08-17 19:22:31",
                    "action": "logout"
                },
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
                    "uuid":"2772b5fa-30a2-4dc8-9c13-76003d42a2da",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "add user weichen"
                },
                {
                    "uuid":"2772b5fa-30a2-4dc8-9c13-76003d42a2da",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "add user wanfeng"
                },
                {
                    "uuid":"2772b5fa-30a2-4dc8-9c13-76003d42a2da",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "modify permissions of user weichen"
                },
                {
                    "uuid":"2772b5fa-30a2-4dc8-9c13-76003d42a2da",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "add group dev"
                },
                {
                    "uuid":"2772b5fa-30a2-4dc8-9c13-76003d42a2da",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "add app jenkins"
                },
                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "add app nodejs"
                },
                                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "add user fangj"
                },
                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "add group sales"
                },
                                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "add group devops"
                },
                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "add permission to group devops"
                },
                                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "delete group devops"
                },
                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "add idp ldap"
                },
                                {
                    "uuid":"38c2203f-a9ba-4da8-9e91-349b75cb665f",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "modify idp ldap settings"
                },
                {
                    "uuid":"30c04d01-a21a-4567-9161-068c487c1e82",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "delete idp ldap"
                },
                                {
                    "uuid":"30c04d01-a21a-4567-9161-068c487c1e82",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "add idp azure-ad"
                },
                {
                    "uuid":"30c04d01-a21a-4567-9161-068c487c1e82",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "modify idp azure-ad settings"
                },
                                {
                    "uuid":"30c04d01-a21a-4567-9161-068c487c1e82",
                    "timestamp":"2021-08-17 19:02:03",
                    "action": "add app alicloud"
                },
                {
                    "uuid":"30c04d01-a21a-4567-9161-068c487c1e82",
                    "timestamp":"2021-08-17 19:05:23",
                    "action": "delete app alicloud"
                }
            ]
        }
        return Response(result)
