from rest_framework import serializers
from posts.models import Post, Comment
from django.contrib.auth import get_user_model
from posts.views import r
from api.users_api.serializers import UserPublicSerializer
from rest_framework import serializers
from posts.models import Comment

User = get_user_model()

class LikeSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField()
    is_liked = serializers.BooleanField()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'parent', 'time_create', 'time_update')

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = UserPublicSerializer(read_only=True)
    # saved = serializers.StringRelatedField(many=True)
    status = serializers.ChoiceField(choices=Post.Status.choices, source="get_status_display")
    count_views = serializers.SerializerMethodField()
    def get_count_views(self, obj):
        return r.get("post:%s:views" % obj.id)
    class Meta:
        model = Post
        fields = ('id', 'name', 'content', 'time_create', 'time_update', 'author', 'saved', 'liked', 'status', 'photo', 'count_views', 'comments')
