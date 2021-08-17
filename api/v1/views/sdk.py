from api.v1.serializers.sdk import SDKSerializer
from rest_framework.permissions import AllowAny
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication
from common.paginator import DefaultListPaginator
from rest_framework import generics
from openapi.utils import extend_schema


@extend_schema(roles=['tenant admin', 'global admin'], tags=['tenant'])
class SdkView(generics.ListAPIView):

    permission_classes = [AllowAny]
    authentication_classes = [ExpiringTokenAuthentication]

    pagination_class = DefaultListPaginator
    serializer_class = SDKSerializer

    def get_queryset(self):
        return [
            {
                "name":"React Native",
                "description":"一键支持Native端社会化登录",
            },
            {
                "name":"JavaScript",
                "description":"支持JavaScript/NodeJS/eXPRESS.JS",
            },
            {
                "name":"Node.js",
                "description":"支持JavaScript/NodeJS/eXPRESS.JS",
            },
            {
                "name":"Android",
                "description":"支持jdk1.8+",
            }
        ]