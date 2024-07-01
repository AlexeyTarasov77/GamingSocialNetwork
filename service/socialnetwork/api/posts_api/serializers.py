from core.redis_connection import r
from django.contrib.auth import get_user_model
from posts.models import Comment, Post
from rest_framework import serializers

from api.users_api.serializers import UserPublicSerializer

User = get_user_model()


class LikeSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField()
    is_liked = serializers.BooleanField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content", "parent", "time_create", "time_update")


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = UserPublicSerializer(read_only=True)
    # saved = serializers.StringRelatedField(many=True)
    count_views = serializers.SerializerMethodField()

    def get_count_views(self, obj):
        return r.get("post:%s:views" % obj.id)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "time_create",
            "time_update",
            "author",
            "saved",
            "liked",
            "tag_list",
            "status",
            "photo",
            "count_views",
            "comments",
        )
