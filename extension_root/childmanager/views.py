from drf_spectacular.utils import extend_schema
from common.code import Code
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.http.response import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.http.response import JsonResponse
from common.paginator import DefaultListPaginator
from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication
from extension_root.childmanager.models import ChildManager
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from openapi.utils import extend_schema
from extension_root.childmanager.serializers import(
    ChildManagerListSerializer, ChildManagerSerializer
)
from inventory.models import User
from tenant.models import Tenant


@extend_schema(roles=['tenant admin', 'global admin'], tags=['admin'])
class ChildManagerListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = ChildManagerListSerializer
    pagination_class = DefaultListPaginator

    def get_queryset(self):
        tenant_uuid = self.kwargs['tenant_uuid']
        kwargs = {
            'tenant__uuid': tenant_uuid,
        }
        childmanagers = ChildManager.valid_objects.filter(**kwargs).order_by('id')
        return childmanagers


@extend_schema(roles=['tenant admin', 'global admin'], tags=['admin'])
class ChildManagerCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = ChildManagerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = Tenant.objects.filter(uuid=self.kwargs['tenant_uuid']).first()
        return context


@extend_schema(roles=['tenant admin', 'global admin'], tags=['admin'])
class ChildManagerDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = ChildManagerSerializer

    def get_object(self):
        tenant_uuid = self.kwargs['tenant_uuid']
        kwargs = {
            'tenant__uuid': tenant_uuid,
            'uuid': self.kwargs['childmanager_uuid'],
        }

        obj = ChildManager.valid_objects.filter(**kwargs).first()
        return obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = Tenant.objects.filter(uuid=self.kwargs['tenant_uuid']).first()
        return context