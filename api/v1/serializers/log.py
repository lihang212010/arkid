from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

class LogSerializer(serializers.Serializer):

    uuid = serializers.CharField(
        read_only=True,
        label=_("唯一标识符")
    )
    timestamp = serializers.CharField(
        read_only=True,
        label=_("时间")
    )
    action = serializers.CharField(
        read_only=True,
        label=_("操作")
    )

    class Meta:

        fields = (
            'username',
            'timestamp',
            'action',
        )
