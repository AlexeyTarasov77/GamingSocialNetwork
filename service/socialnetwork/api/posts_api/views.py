from . import serializers as s
from rest_framework import generics, views
from posts.models import Post, Comment
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from posts.mixins import ListPostsQuerySetMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

class PostsViewSet(ListPostsQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = s.PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeAPIView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Вернуть данные только если пользователь аутентифицирован

    def post(self, request, *args, **kwargs):
        obj_id = request.POST.get("object_id")  # получить id текущего поста из запроса
        obj = self.get_object(obj_id)

        if request.user in obj.liked.all():  # если текущий пользователь уже лайкал пост
            obj.liked.remove(request.user)  # удалить его из отношения
            data = {
                "likes_count": obj.liked.count(),
                "is_liked": False,
            }  # сформированная дата для отправки на клиент
        else:  # если пользователя нет в таблице отношений добавить его и сформировать другую дату
            obj.liked.add(request.user)
            data = {"likes_count": obj.liked.count(), "is_liked": True}
        serializer = s.LikeSerializer(data)  # сериализовать данные в json формат
        return Response(serializer.data)  # вернуть на клиент сериализованные данные

    def get_object(obj_id):
        pass


class LikePostAPIView(LikeAPIView):
    def get_object(self, obj_id):
        return get_object_or_404(Post, id=obj_id)


class LikeCommentAPIView(LikeAPIView):
    def get_object(self, obj_id):
        return get_object_or_404(Comment, id=obj_id)


class SavePostAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.published.all()
    lookup_url_kwarg = "post_id"

    def patch(self, request, post_id):
        post = self.get_object()
        if request.user in post.saved.all():
            post.saved.remove(request.user)
            return Response({"is_saved": False})
        else:
            post.saved.add(request.user)
            return Response({"is_saved": True})


class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = s.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs.get("post_id", None),
            parent_id=self.request.data.get("parent") or None,
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
            obj.is_root_node()
            or obj.get_root().author.username
            == obj.author.username
        )
        comment_data["author_image"] = obj.author.profile.get_profile_image()
        return Response(comment_data, status=status.HTTP_201_CREATED)


