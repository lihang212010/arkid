from rest_framework import serializers


class LogSerializer(serializers.Serializer):

    uuid = serializers.CharField(read_only=True)
    timestamp = serializers.CharField(read_only=True)
    action = serializers.CharField(read_only=True)

    class Meta:

        fields = (
            'username',
            'timestamp',
            'action',
        )
