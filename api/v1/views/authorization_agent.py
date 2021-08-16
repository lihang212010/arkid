from authorization_agent.models import AuthorizationAgent
from rest_framework import viewsets
from api.v1.serializers.authorization_agent import AuthorizationAgentSerializer
from rest_framework.decorators import action
from runtime import get_app_runtime
from openapi.utils import extend_schema
from common.paginator import DefaultListPaginator


@extend_schema(
    roles=['tenant admin', 'global admin'], tags = ['authorizationAgent']
)
class AuthorizationAgentViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AuthorizationAgentSerializer
    pagination_class = DefaultListPaginator

    def get_queryset(self):
        runtime = get_app_runtime()
        objs = runtime.authorization_agents
        return objs

    def get_object(self):
        runtime = get_app_runtime()

        obj: AuthorizationAgent
        objs = runtime.authorization_agents
        for obj in objs:
            if obj.id == self.kwargs['pk']:
                return obj

        return None
        
