from .serializers import PostSerializer
from rest_framework import generics
from posts.models import Post
from rest_framework import viewsets
from posts.mixins import ListPostsQuerySetMixin
from django.urls import reverse_lazy


class PostsViewSet(ListPostsQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# class ListPostsAPIView(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.published.all()

# list_posts_api_view = ListPostsAPIView.as_view()

# class DetailPostAPIView(generics.RetrieveAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.published.all()

# detail_post_api_view = DetailPostAPIView.as_view()


