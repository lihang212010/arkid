from runtime import Runtime
from common.extension import InMemExtension, ExtensionBaseSerializer
from .provider import OAuth2AppTypeProvider
from .serializers import OAuth2AppSerializer, OIDCAppSerializer


class OAuthAuthorizationServerExtension(InMemExtension):

    def start(self, runtime: Runtime, *args, **kwargs):
        # Contribute OAuth Authentication Server & parameters
        runtime.register_authorization_server(
            id='oauth2',
            name='OAuth2',
            description='OAuth2',
        )
        runtime.register_authorization_server(
            id='oidc',
            name='OpenID Connect',
            description='OpenID Connect',
        )
        runtime.register_app_type(
            key='OAuth2',
            name='OAuth2',
            provider=OAuth2AppTypeProvider,
            serializer=OAuth2AppSerializer
        )
        runtime.register_app_type(
            key='OIDC',
            name='OpenID Connect',
            provider=OAuth2AppTypeProvider,
            serializer=OIDCAppSerializer
        )

        super().start(runtime=runtime, *args, **kwargs)

    def teardown(self, runtime: Runtime, *args, **kwargs):
        # Contribute OAuth Authentication Server & parameters
        runtime.logout_authorization_server(
            id='oauth2',
            name='OAuth2',
            description='OAuth2',
        )
        runtime.logout_authorization_server(
            id='oidc',
            name='OpenID Connect',
            description='OpenID Connect',
        )
        runtime.logout_app_type(
            key='OAuth2',
            name='OAuth2',
            provider=OAuth2AppTypeProvider,
            serializer=OAuth2AppSerializer
        )
        runtime.logout_app_type(
            key='OIDC',
            name='OpenID Connect',
            provider=OAuth2AppTypeProvider,
            serializer=OIDCAppSerializer
        )

extension = OAuthAuthorizationServerExtension(
    scope='tenant',
    type='tenant',
    tags='oauth',
    name='oauth2_authorization_server',
    description='Arkid OAuth2 authorization server',
    version='1.0',
    homepage='https://www.longguikeji.com',
    logo='',
    maintainer='hanbin@jinji-inc.com',
)
