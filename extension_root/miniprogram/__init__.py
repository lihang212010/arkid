from common.extension import InMemExtension
from .constants import KEY
from .provider import MiniProgramExternalIdpProvider
from .serializers import MiniProgramExternalIdpSerializer


class MiniProgramExtension(InMemExtension):

    def start(self, runtime, *args, **kwargs):
        runtime.register_external_idp(
            key=KEY,
            name='微信小程序',
            description='一种不需要下载安装即可使用的应用，它实现了应用“触手可及”的梦想',
            provider=MiniProgramExternalIdpProvider,
            serializer=MiniProgramExternalIdpSerializer,
        )
        super().start(runtime, *args, **kwargs)


extension = MiniProgramExtension(
    name='miniprogram',
    tags='login',
    scope='tenant',
    type='tenant',
    description='微信小程序',
    version='1.0',
    homepage='https://www.longguikeji.com',
    logo='',
    maintainer='insfocus@gmail.com',
)