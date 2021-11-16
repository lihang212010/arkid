from common.paginator import DefaultListPaginator
from api.v1.views.base import BaseViewSet
from drf_spectacular.utils import extend_schema_view
from openapi.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication
from ..models import ApplicationMultipleIp
from ..serializers import BaseApplicationMultipleIpSerializer
from app.models import App
from django.http.response import JsonResponse


@extend_schema_view(
    list=extend_schema(
        roles=['tenant admin', 'global admin', 'general user'],
    ),
    retrieve=extend_schema(roles=['tenant admin', 'global admin']),
    create=extend_schema(roles=['tenant admin', 'global admin']),
    update=extend_schema(roles=['tenant admin', 'global admin']),
    destroy=extend_schema(roles=['tenant admin', 'global admin']),
    partial_update=extend_schema(roles=['tenant admin', 'global admin']),
)
class ApplicationMultipleIpViewSet(BaseViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = BaseApplicationMultipleIpSerializer
    pagination_class = DefaultListPaginator

    def get_queryset(self):
        context = self.get_serializer_context()
        tenant = context['tenant']
        qs = ApplicationMultipleIp.active_objects.filter(
            app__tenant=tenant).order_by('id')
        return qs

    def get_object(self):
        uuid = self.kwargs['pk']
        context = self.get_serializer_context()
        tenant = context['tenant']

        return (
            ApplicationMultipleIp.active_objects.filter(
                app__tenant=tenant,
                uuid=uuid,
            )
            .order_by('id')
            .first()
        )

    def create(self, request, *args, **kwargs):
        app_id=request.data.get("app")
        app = App.active_objects.get(uuid=app_id)
        amip = ApplicationMultipleIp(
            app = app,
            ip_regx = request.data.get("ip_regx"),
            ip = request.data.get("ip")
        )
        amip.save()
        return JsonResponse(
            data={
                "status": 200,
                "data": BaseApplicationMultipleIpSerializer(instance=amip).data
            }
        )