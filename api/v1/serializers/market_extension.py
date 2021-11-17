
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class MarketPlaceExtensionSerializer(serializers.Serializer):

    name = serializers.CharField()
    description = serializers.CharField()
    version = serializers.CharField()
    homepage = serializers.CharField()
    logo = serializers.CharField()
    maintainer = serializers.CharField()
    tags = serializers.CharField()
    type = serializers.CharField()
    scope = serializers.CharField()
    is_install = serializers.BooleanField()

    # class Meta:

    #     fields = (
    #         'id',
    #         'uuid',
    #         'name',
    #         'url',
    #         'description',
    #     )


class MarketPlaceExtensionTagsSerializer(serializers.Serializer):

    data = serializers.ListField(child=serializers.CharField(), label=_('标签'))
