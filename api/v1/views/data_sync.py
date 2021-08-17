from .base import BaseViewSet
from api.v1.serializers.data_sync import (
    DataSyncConfigSerializer,
    DataSyncConfigListSerializer,
    DingDingDataSyncConfigListSerializer,
    WeiChatDataSyncConfigListSerializer,
    ScimDataSyncConfigListSerializer,
)
from django.http.response import JsonResponse
from openapi.utils import extend_schema
from drf_spectacular.utils import PolymorphicProxySerializer
from common.paginator import DefaultListPaginator
from .base import BaseViewSet
from data_sync.models import DataSyncConfig
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication
from common.code import Code

serializer_map = {
    'dingding': DingDingDataSyncConfigListSerializer,
    'weichat': WeiChatDataSyncConfigListSerializer,
    'scim': ScimDataSyncConfigListSerializer,
}
DataSyncConfigPolymorphicProxySerializer = PolymorphicProxySerializer(
    component_name='DataSyncConfigPolymorphicProxySerializer',
    serializers=serializer_map,
    resource_type_field_name='type',
)


@extend_schema_view(
    destroy=extend_schema(roles=['tenant admin', 'global admin']),
    partial_update=extend_schema(roles=['tenant admin', 'global admin']),
)
@extend_schema(tags=['data_sync'])
class DataSyncConfigViewSet(BaseViewSet):

    model = DataSyncConfig

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    serializer_class = DataSyncConfigSerializer
    pagination_class = DefaultListPaginator

    def get_queryset(self):
        context = self.get_serializer_context()
        tenant = context['tenant']

        kwargs = {
            'tenant': tenant,
        }

        return DataSyncConfig.valid_objects.filter(**kwargs)

    def get_object(self):
        context = self.get_serializer_context()
        tenant = context['tenant']

        kwargs = {
            'tenant': tenant,
            'uuid': self.kwargs['pk'],
        }

        obj = DataSyncConfig.valid_objects.filter(**kwargs).first()
        return obj

    @extend_schema(
        roles=['tenant admin', 'global admin'], responses=DataSyncConfigListSerializer
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        roles=['tenant admin', 'global admin'],
        request=DataSyncConfigPolymorphicProxySerializer,
        responses=DataSyncConfigPolymorphicProxySerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        roles=['tenant admin', 'global admin'],
        request=DataSyncConfigPolymorphicProxySerializer,
        responses=DataSyncConfigPolymorphicProxySerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        roles=['tenant admin', 'global admin'],
        responses=DataSyncConfigPolymorphicProxySerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
