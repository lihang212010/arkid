from rest_framework import serializers
from api.v1.fields.custom import (
    create_title_field,
    create_hint_field
)

class LogSerializer(serializers.Serializer):

    uuid = serializers.CharField(read_only=True, label="唯一标识符")
    timestamp = serializers.CharField(read_only=True, label="时间戳")
    action = serializers.CharField(read_only=True, label="操作")

    class Meta:

        fields = (
            'username',
            'timestamp',
            'action',
        )
