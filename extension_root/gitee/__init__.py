from common.extension import InMemExtension
from .serializers import GiteeExternalIdpSerializer
from .provider import GiteeExternalIdpProvider
from runtime import Runtime
from .constants import KEY


class GiteeExternalIdpExtension(InMemExtension):

    def start(self, runtime: Runtime, *args, **kwargs):
        runtime.register_external_idp(
            key=KEY,
            name="Gitee",
            description="Gitee External idP",
            provider=GiteeExternalIdpProvider,
            serializer=GiteeExternalIdpSerializer,
        )
        super().start(runtime=runtime, *args, **kwargs)
    
    def teardown(self, runtime: Runtime, *args, **kwargs):
        runtime.logout_external_idp(
            key=KEY,
            name="Gitee",
            description="Gitee External idP",
            provider=GiteeExternalIdpProvider,
            serializer=GiteeExternalIdpSerializer,
        )


extension = GiteeExternalIdpExtension(
    name="gitee",
    tags='login',
    scope='tenant',
    type='tenant',
    description="gitee as the external idP",
    version="1.0",
    homepage="https://www.longguikeji.com",
    logo="",
    maintainer="hanbin@jinji-inc.com",
)
