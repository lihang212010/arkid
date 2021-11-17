from .base import BaseViewSet
from api.v1.serializers.extension import ExtensionSerializer, ExtensionListSerializer
from openapi.utils import extend_schema
from drf_spectacular.utils import PolymorphicProxySerializer
from extension.models import Extension
from runtime import get_app_runtime
from django.http.response import JsonResponse
from drf_spectacular.utils import extend_schema_view, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication
from django.utils.translation import gettext_lazy as _
from extension.utils import reload_extension
from common.code import Code


ExtensionPolymorphicProxySerializer = PolymorphicProxySerializer(
    component_name='ExtensionPolymorphicProxySerializer',
    serializers=get_app_runtime().extension_serializers,
    resource_type_field_name='type'
)

@extend_schema_view(
    list=extend_schema(
        roles=['global admin'],
        parameters=[
            OpenApiParameter(
                name='tags',
                type={'type': 'string'},
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name='type',
                type={'type': 'string'},
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name='scope',
                type={'type': 'string'},
                location=OpenApiParameter.QUERY,
                required=False,
            ),
        ]),
    destroy=extend_schema(roles=['global admin']),
    partial_update=extend_schema(roles=['global admin']),
)
@extend_schema(tags = ['extension'])
class ExtensionViewSet(BaseViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
    serializer_class = ExtensionSerializer

    def get_queryset(self):
        from extension.utils import find_available_extensions
        tags = self.request.query_params.get('tags', '')
        extension_type = self.request.query_params.get('type', '')
        scope = self.request.query_params.get('scope', '')
        if tags or extension_type or scope:
            extensions = find_available_extensions()
            result = []
            for extension in extensions:
                if tags and extension_type and scope:
                    tags_cp = tags.split(',')
                    extension_type_cp = extension_type.split(',')
                    scope_cp = scope.split(',')
                    if tags_cp and extension.tags in tags_cp and extension_type_cp and extension.type in extension_type_cp and scope_cp and extension.scope in scope_cp:
                        result.append(extension)
                elif tags and extension_type:
                    tags_cp = tags.split(',')
                    extension_type_cp = extension_type.split(',')
                    if tags_cp and extension.tags in tags_cp and extension_type_cp and extension.type in extension_type_cp:
                        result.append(extension)
                elif tags and scope:
                    tags_cp = tags.split(',')
                    scope_cp = scope.split(',')
                    if tags_cp and extension.tags in tags_cp and scope_cp and extension.scope in scope_cp:
                        result.append(extension)
                elif tags:
                    tags_cp = tags.split(',')
                    if tags_cp and extension.tags in tags_cp:
                        result.append(extension)
                elif scope:
                    scope_cp = scope.split(',')
                    if scope_cp and extension.scope in scope_cp:
                        result.append(extension)
                elif extension_type:
                    extension_type_cp = extension_type.split(',')
                    if extension_type_cp and extension.type in extension_type_cp:
                        result.append(extension)
            extensions = result
            exs = Extension.valid_objects.filter()
            uuids = []
            for ex in exs:
                for extension in extensions:
                    if extension.name == ex.type:
                        uuids.append(ex.uuid)
            return exs.filter(uuid__in=uuids)
        else:
            return Extension.valid_objects.filter()

    def get_object(self):
        o = Extension.valid_objects.filter(
            uuid=self.kwargs['pk']
        ).first()

        return o

    @extend_schema(
        responses=ExtensionListSerializer
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        roles=['global admin'],
        request=ExtensionPolymorphicProxySerializer,
        responses=ExtensionPolymorphicProxySerializer,
    )
    def update(self, request, *args, **kwargs):
        data = request.data.get('data','')
        data_path = data.get('data_path', '')
        if data_path:
            if '../' in data_path or './' in data_path:
                return JsonResponse(data={
                    'error': Code.DATA_PATH_ERROR.value,
                    'message': _('data_path format error'),
                })
        return super().update(request, *args, **kwargs)

    @extend_schema(
        roles=['global admin'],
        request=ExtensionPolymorphicProxySerializer,
        responses=ExtensionPolymorphicProxySerializer,
    )
    def create(self, request, *args, **kwargs):
        data = request.data.get('data','')
        data_path = data.get('data_path', '')
        if data_path:
            if '../' in data_path or './' in data_path:
                return JsonResponse(data={
                    'error': Code.DATA_PATH_ERROR.value,
                    'message': _('data_path format error'),
                })
        return super().create(request, *args, **kwargs)

    @extend_schema(
        roles=['global admin'],
        responses=ExtensionPolymorphicProxySerializer
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        roles=['global admin'],
    )
    def destroy(self, request, *args, **kwargs):
        o = self.get_object()
        result = super(ExtensionViewSet, self).destroy(request, *args, **kwargs)
        reload_extension(o.type, False)
        return result
