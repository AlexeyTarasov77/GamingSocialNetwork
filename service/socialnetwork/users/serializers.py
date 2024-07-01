from rest_framework import serializers


class SubscribeSerializer(serializers.Serializer):
    subsribed = serializers.BooleanField()
