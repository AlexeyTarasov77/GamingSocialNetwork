from rest_framework import serializers
from .models import Comment

class LikeSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField()
    is_liked = serializers.BooleanField()
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'parent', 'time_create', 'time_update']