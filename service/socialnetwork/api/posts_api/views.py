from abc import abstractmethod

from django.shortcuts import get_object_or_404
from posts.mixins import ListPostsQuerySetMixin
from posts.models import Comment, Post
from posts.services.posts_service import PostsService
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response

from . import serializers as s


class PostsViewSet(ListPostsQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = s.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeAPIView(views.APIView):
    """
    Base APIView for liking and unliking objects
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]  # Вернуть данные только если пользователь аутентифицирован

    def post(self, request, *args, **kwargs):
        obj = self.get_object(request.POST.get("object_id"))  # получить id текущего поста из запроса
        is_liked = PostsService.like_post(obj, request.user)
        data = {"is_liked": is_liked, "likes_count": obj.liked.count()}
        serializer = s.LikeSerializer(data)  # сериализовать данные в json формат
        return Response(serializer.data)  # вернуть на клиент сериализованные данные

    @abstractmethod
    def get_object(self, obj_id):
        """Base method which will be redefined in subclasses"""
        pass


class LikePostAPIView(LikeAPIView):
    """View for liking and unliking posts"""

    def get_object(self, obj_id) -> Post:
        return get_object_or_404(Post, id=obj_id)


class LikeCommentAPIView(LikeAPIView):
    """View for liking and unliking comments"""

    def get_object(self, obj_id) -> Comment:
        return get_object_or_404(Comment, id=obj_id)


class SavePostAPIView(generics.GenericAPIView):
    queryset = Post.published.all()
    lookup_url_kwarg = "post_id"

    def patch(self, request, post_id) -> Response:
        post = self.get_object()
        is_saved = PostsService.save_post(post, request.user)
        data = {"is_saved": is_saved}
        return Response(data)


class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = s.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs.get("post_id", None),
            parent_id=self.request.data.get("parent", None) or None,
            author=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        comment_data = serializer.data
        obj = serializer.instance
        comment_data["author"] = obj.author.username
        comment_data["is_child"] = obj.is_child_node()
        comment_data["by_author"] = (
            obj.is_root_node() or obj.get_root().author.username == obj.author.username
        )
        comment_data["author_image"] = obj.author.profile.get_image()
        return Response(comment_data, status=status.HTTP_201_CREATED)
        return Response(comment_data, status=status.HTTP_201_CREATED)
