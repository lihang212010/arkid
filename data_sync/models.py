from common.model import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class DataSyncConfig(BaseModel):
    SYNC_TYPES = (
        ('dingding', _('Ding Ding')),
        ('weichat', _('Enterprise WeiChat')),
        ('scim', _('Scim')),
    )

    SYNC_DIRECTIONS = (
        ('upstream', _('To ArkID')),
        ('downstream', _('From ArkID')),
    )

    STATUS_CHOICES = (
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    )

    tenant = models.ForeignKey(
        'tenant.Tenant', blank=False, null=True, on_delete=models.PROTECT
    )
    type = models.CharField(
        choices=SYNC_TYPES, max_length=32, verbose_name=_('Data Sync Type')
    )
    sync_direction = models.CharField(
        choices=SYNC_DIRECTIONS, max_length=32, verbose_name=_('Sync Direction')
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=32)
    mapping = models.JSONField(default=dict)
    data = models.JSONField(default=dict)
