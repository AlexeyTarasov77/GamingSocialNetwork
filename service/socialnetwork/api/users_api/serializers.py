from rest_framework import serializers

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()