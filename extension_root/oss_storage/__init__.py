from rest_framework.serializers import Serializer
from runtime import Runtime
from common.extension import InMemExtension
from .provider import OSSStorageProvider
from .serializers import OSSStorageSerializer


class OSSStorageExtension(InMemExtension):

    def start(self, runtime: Runtime, *args, **kwargs):
        provider = OSSStorageProvider()
        provider.domain = self.config('domain')
        provider.bucket = self.config('bucket')
        provider.access_key = self.config('access_key')
        provider.secret_key = self.config('secret_key')
        provider.endpoint = self.config('endpoint', 'https://oss-cn-beijing.aliyuncs.com')

        runtime.register_storage_provider(
            provider=provider,
        )

        super().start(runtime=runtime, *args, **kwargs)

    def teardown(self, runtime: Runtime, *args, **kwargs):
        provider = OSSStorageProvider()
        provider.domain = self.config('domain')
        provider.bucket = self.config('bucket')
        provider.access_key = self.config('access_key')
        provider.secret_key = self.config('secret_key')
        provider.endpoint = self.config('endpoint', 'https://oss-cn-beijing.aliyuncs.com')

        runtime.logout_storage_provider(
            provider=provider,
        )


extension = OSSStorageExtension(
    name='oss_storage',
    tags='storage',
    description='Aliyun OSS based storage solution',
    version='1.0',
    logo='',
    maintainer='hanbin@jinji-inc.com',
    homepage='https://www.longguikeji.com',
    contact='rock@longguikeji.com',
    serializer=OSSStorageSerializer,
    scope='global',
    type='global',
)
