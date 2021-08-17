from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class SDKSerializer(serializers.Serializer):

    name = serializers.CharField(
        label=_("名称")
    )

    description = serializers.CharField(
        label=_("描述")
    )