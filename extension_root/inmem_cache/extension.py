from runtime import Runtime
from common.extension import InMemExtension
from .provider import InMemCacheProvider


class InMemCacheExtension(InMemExtension):    

    def start(self, runtime: Runtime, *args, **kwargs):
        cache_provider = InMemCacheProvider()

        runtime.cache_provider = cache_provider
        print('>>>', runtime.cache_provider)

        super().start(runtime=runtime, *args, **kwargs)