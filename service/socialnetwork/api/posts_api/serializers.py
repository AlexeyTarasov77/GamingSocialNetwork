from rest_framework import serializers
from posts.models import Post
from django.contrib.auth import get_user_model
from posts.views import r

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    # saved = serializers.StringRelatedField(many=True)
    status = serializers.ChoiceField(choices=Post.Status.choices)
    count_views = serializers.SerializerMethodField()
    def get_count_views(self, obj):
        return r.get("post:%s:views" % obj.id)
    class Meta:
        model = Post
        fields = ('id', 'name', 'content', 'time_create', 'time_update', 'author', 'saved', 'liked', 'status', 'photo', 'count_views',)