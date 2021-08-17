from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

class AuthorizationServerSerializer(serializers.Serializer):

    id = serializers.CharField(
        label=_("唯一标识")
    )
    name = serializers.CharField(
        label=_("名称")
    )
    description = serializers.CharField(
        label=_("描述")
    )
