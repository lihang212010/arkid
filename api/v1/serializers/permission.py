from lib.dynamic_fields_model_serializer import DynamicFieldsModelSerializer
from inventory.models import Permission
from rest_framework import serializers

class PermissionSerializer(DynamicFieldsModelSerializer):

    uuid = serializers.CharField(read_only=True)
    codename = serializers.CharField(read_only=True)

    class Meta:
        model = Permission

        fields = (
            'uuid',
            'name',
            'codename',
        )


class PermissionGroupSerializer(serializers.Serializer):

    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    permissions = serializers.ListField(child=serializers.CharField(), read_only=True)
    permission_groups = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:

        fields = (
            'uuid',
            'name',
            'permissions',
            'permission_groups',
        )


class PermissionGroupSerializer(serializers.Serializer):

    username = serializers.CharField(read_only=True)
    permissions = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:

        fields = (
            'username',
            'permissions',
        )