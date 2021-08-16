from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.v1.serializers.permission import (
    PermissionSerializer, PermissionGroupSerializer
)
from common.paginator import DefaultListPaginator
from openapi.utils import extend_schema
from .base import BaseTenantViewSet
from inventory.models import Permission
from rest_framework import viewsets
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication


@extend_schema(
    roles=['tenant admin', 'global admin'],
    tags = ['permission']
)
class PermissionViewSet(BaseTenantViewSet, viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = PermissionSerializer
    pagination_class = DefaultListPaginator

    def get_queryset(self):
        context = self.get_serializer_context()
        tenant = context['tenant']

        objs = Permission.objects.filter(
            tenant=tenant,
        )

        return objs

    def get_object(self):
        context = self.get_serializer_context()
        tenant = context['tenant']

        kwargs = {
            'tenant': tenant,
            'uuid': self.kwargs['pk'],
        }

        obj = Permission.valid_objects.filter(**kwargs).first()
        return obj


@extend_schema(
    roles=['tenant admin', 'global admin'],
    tags = ['permission']
)
class PermissionGroupViewSet(BaseTenantViewSet, viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = PermissionGroupSerializer
    pagination_class = DefaultListPaginator

    def list(self, request, parent_lookup_tenant):
        result = {
            "count":2,
            "next":None,
            "previous":None,
            "results":[
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba85144b",
                    "name":"",
                    "permissions":[
                        "Can access app oidc",
                        "Can access app cas"
                    ],
                    "permission_groups":[

                    ]
                },
                {
                    "uuid":"5dc4b555-7795-4729-878f-703aba85144a",
                    "name":"",
                    "permissions":[

                    ],
                    "permission_groups":[
                        "5dc4b555-7795-4729-878f-703aba85144b"
                    ]
                }
            ]
        }
        return Response(result)

    def retrieve(self, request, parent_lookup_tenant, pk=None):
        result = {
            "uuid":"5dc4b555-7795-4729-878f-703aba85144a",
            "name":"",
            "permissions":[

            ],
            "permission_groups":[
                "5dc4b555-7795-4729-878f-703aba85144b"
            ]
        }
        return Response(result)


@extend_schema(
    roles=['tenant admin', 'global admin'],
    tags = ['permission']
)
class PermissionManageViewSet(BaseTenantViewSet, viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = PermissionGroupSerializer
    pagination_class = DefaultListPaginator

    def list(self, request, parent_lookup_tenant):
        result = {
            "count":2,
            "next":None,
            "previous":None,
            "results":[
                {
                    "username":"admin",
                    "permissions":[
                        "manage_app",
                        "manage_tenant"
                    ]
                },
                {
                    "username":"tenant1",
                    "permissions":[
                        "manage_tenant1"
                    ]
                }
            ]
        }
        return Response(result)

    def retrieve(self, request, parent_lookup_tenant, pk=None):
        result = {
            "username":"admin",
            "permissions":[
                "manage_app",
                "manage_tenant"
            ]
        }
        return Response(result)