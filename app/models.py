from django.db import models
from common.model import BaseModel
from tenant.models import Tenant
from django.utils.translation import gettext_lazy as _


class App(BaseModel):

    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.PROTECT,
        verbose_name=_("租户")
    )
    name = models.CharField(
        max_length=128,
        verbose_name=_("名称")
    )
    url = models.CharField(
        max_length=1024, 
        blank=True,
        verbose_name=_("链接")
    )
    logo = models.FileField(
        blank=True, 
        null=True,
        verbose_name=_("图标")
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("描述")
    )
    type = models.CharField(
        max_length=128, 
        verbose_name=_('应用类型')
    )
    data = models.JSONField(
        blank=True, 
        default=dict,
        verbose_name=_("额外数据")
    )
    auth_tmpl = models.TextField(
        blank=True, 
        null=True, 
        default='',
        verbose_name=_("认证模板")
    )

    def __str__(self) -> str:
        return f'Tenant: {self.tenant.name}, App: {self.name}'

    @property
    def app_type(self):
        from runtime import get_app_runtime

        r = get_app_runtime()
        return r.app_types

    @property
    def access_perm_code(self):
        return f'app_access_{self.uuid}'

    def as_dict(self):
        return {
            'uuid': self.uuid.hex,
            'is_del': self.is_del,
            'is_active': self.is_active,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'type': self.type,
            'data': self.data,
        }


# class AuthServer(BaseModel):

#     TYPE_CHOICES = (
#         (0, 'Unknown'),
#         (1, 'OAuth 2.0'),
#         (2, 'LDAP'),
#         (3, 'OIDC'),
#         (4, 'SAML'),
#         (5, 'CAS WEB'),
#         (6, 'SWA'),
#         (7, 'WS-Fed'),
#     )

#     # tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
#     app = models.ForeignKey(App, on_delete=models.PROTECT)
#     type = models.IntegerField(choices=TYPE_CHOICES, default=0)
