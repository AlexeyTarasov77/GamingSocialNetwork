from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("", views.PostsViewSet, basename="posts")

app_name = "posts"

urlpatterns = [
    # path("", include(router.urls)),
    path("like-post/", views.LikePostAPIView.as_view(), name="like-post"),
    path("like-comment/", views.LikeCommentAPIView.as_view(), name="like-comment"),
    path(
        "comment-post/<int:post_id>/",
        views.CreateCommentAPIView.as_view(),
        name="comment-post",
    ),
    path("save-post/<int:post_id>/", views.SavePostAPIView.as_view(), name="save-post"),
    path("", include(router.urls)),
]
