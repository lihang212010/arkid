"""
LDAP 插件处理
"""
from common.extension import InMemExtension
from runtime import Runtime

class LdapServerExtension(InMemExtension):
    """
    插件
    """

    def start(self, runtime: Runtime, *args, **kwargs):

        runtime.register_authorization_agent(
            id='microsoft_ad',
            name='微软AD',
            description='微软AD',
        )

        super().start(runtime=runtime, *args, **kwargs)

    def teardown(self, runtime: Runtime, *args, **kwargs):  # pylint: disable=unused-argument
        runtime.logout_authorization_agent(
            id='microsoft_ad',
            name='微软AD',
            description='微软AD',
        )


extension = LdapServerExtension(
    tags='ldap',
    name="microsoft_ad",
    scope='tenant',
    type='tenant',
    description="微软AD",
    version="1.0",
    homepage="https://www.longguikeji.com",
    logo="",
    maintainer="北京龙归科技有限公司",
)
