from lib.dynamic_fields_model_serializer import DynamicFieldsModelSerializer
from inventory.models import Permission
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

class PermissionSerializer(DynamicFieldsModelSerializer):

    uuid = serializers.CharField(
        read_only=True,
        label=_("唯一标识")
    )
    codename = serializers.CharField(
        read_only=True,
        label=_("代码")
    )

    class Meta:
        model = Permission

        fields = (
            'uuid',
            'name',
            'codename',
        )


class PermissionGroupSerializer(serializers.Serializer):

    uuid = serializers.CharField(
        read_only=True,
        label=_("唯一标识")
    )
    name = serializers.CharField(
        read_only=True,
        label=_("名称")
    )
    permissions = serializers.ListField(child=serializers.CharField(), read_only=True,label=_("权限列表"))
    permission_groups = serializers.ListField(child=serializers.CharField(), read_only=True,label=_("权限分组列表"))

    class Meta:

        fields = (
            'uuid',
            'name',
            'permissions',
            'permission_groups',
        )


class PermissionGroupSerializer(serializers.Serializer):

    username = serializers.CharField(read_only=True,label=_("用户名"))
    permissions = serializers.ListField(child=serializers.CharField(), read_only=True,label=_("权限列表"))

    class Meta:

        fields = (
            'username',
            'permissions',
        )