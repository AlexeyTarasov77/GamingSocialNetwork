from django.urls import include, path

from . import views

app_name = "posts"

urlpatterns = [
    path("list-posts/", views.ListPosts.as_view(), name="list-posts"),
    path(
        "list-posts/by-tag/<slug:tag_slug>/",
        views.ListPosts.as_view(),
        name="list-posts-by-tag",
    ),
    path("detail-post/<int:post_id>/", views.DetailPost.as_view(), name="detail-post"),
    path("delete-post/<int:pk>/", views.DeletePost.as_view(), name="delete-post"),
    path("update-post/<int:pk>/", views.UpdatePost.as_view(), name="update-post"),
    path("add-post/", views.CreatePost.as_view(), name="add-post"),
    path("share-post/<int:post_id>/", views.share_post, name="share-post"),
]
