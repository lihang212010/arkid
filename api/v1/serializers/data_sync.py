from common.serializer import BaseDynamicFieldModelSerializer
from data_sync.models import DataSyncConfig
from common.provider import ExternalIdpProvider
from rest_framework import serializers
from django.db.models import Max
from django.utils.translation import gettext_lazy as _


class DataSyncConfigSerializer(BaseDynamicFieldModelSerializer):
    type = serializers.ChoiceField(choices=DataSyncConfig.SYNC_TYPES, label=_('同步类型'))
    status = serializers.ChoiceField(
        choices=DataSyncConfig.STATUS_CHOICES, label=_('启用状态')
    )
    sync_direction = serializers.ChoiceField(
        choices=DataSyncConfig.SYNC_DIRECTIONS, label=_('同步方向')
    )

    class Meta:

        model = DataSyncConfig

        fields = (
            'uuid',
            'type',
            'data',
            'sync_direction',
            'status',
            # 'mapping',
        )

    def create(self, validated_data):

        tenant = self.context['tenant']
        sync_type = validated_data.pop('type')
        status = validated_data.pop('status')
        sync_direction = validated_data.pop('sync_direction')
        data = validated_data.pop('data', None)
        sync_config = DataSyncConfig.valid_objects.create(
            type=sync_type,
            status=status,
            sync_direction=sync_direction,
            data=data,
            tenant=tenant,
        )
        return sync_config

    def update(self, instance, validated_data):
        sync_type = validated_data.pop('type')
        status = validated_data.pop('status')
        sync_direction = validated_data.pop('sync_direction')
        data = validated_data.pop('data', {})

        instance.sync_status = sync_type
        instance.status = status
        instance.sync_direction = sync_direction
        instance.data = data

        instance.save()

        return instance


class DataSyncConfigListSerializer(DataSyncConfigSerializer):
    class Meta:
        model = DataSyncConfig

        fields = ('type', 'sync_direction', 'status')


class DingDingConfigSerializer(serializers.Serializer):
    corp_id = serializers.CharField(label=_('企业ID'))
    app_key = serializers.CharField(label=_('钉钉应用的AppKey'))
    app_secret = serializers.CharField(label=_('钉钉应用的AppSecret'))


class DingDingDataSyncConfigListSerializer(DataSyncConfigSerializer):
    data = DingDingConfigSerializer(label=_('配置数据'))


class WeiChatConfigSerializer(serializers.Serializer):
    corp_id = serializers.CharField(label=_('企业ID'))
    secret = serializers.CharField(label=_('企业通讯录密钥 Secret'))
    token = serializers.CharField(label=_('通讯录事件同步 Token'))
    encoding_aes_key = serializers.CharField(label=_('通讯录事件同步EncodingAESKey'))


class WeiChatDataSyncConfigListSerializer(DataSyncConfigSerializer):
    data = WeiChatConfigSerializer(label=_('配置数据'))


class ScimConfigSerializer(serializers.Serializer):
    base_url = serializers.CharField(label=_('Scim服务地址'))
    auth_type = serializers.ChoiceField(
        choices=[('basic', 'Basic Authentication'), ('token', 'Token Authentication')],
        label=_('Scim服务认证方式'),
    )
    token = serializers.CharField(label=_('认证Token'))
    username = serializers.CharField(label=_('Basic认证用户名'))
    password = serializers.CharField(label=_('Basic认证密码'))


class ScimDataSyncConfigListSerializer(DataSyncConfigSerializer):
    data = ScimConfigSerializer(label=_('配置数据'))
