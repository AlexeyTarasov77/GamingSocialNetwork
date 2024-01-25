from rest_framework import serializers

class LikeSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField()
    is_liked = serializers.BooleanField()