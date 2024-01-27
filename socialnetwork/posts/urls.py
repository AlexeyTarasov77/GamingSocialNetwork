from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path("list-posts/", views.ListPosts.as_view(), name="list-posts"),
    path("list-posts/by-tag/<slug:tag_slug>/", views.ListPosts.as_view(), name="list-posts-by-tag"),
    path("detail-post/<int:post_id>/", views.DetailPost.as_view(), name="detail-post"),
    path("delete-post/<int:post_id>/", views.DeletePost.as_view(), name="delete-post"),
    path("update-post/<int:post_id>/", views.UpdatePost.as_view(), name="update-post"),
    path("like-post/", views.LikePostAPIView.as_view(), name="like-post"),
    path("share-post/<int:post_id>/", views.share_post, name="share-post"),
    path("comment-post/<int:post_id>/", views.CreateCommentView.as_view(), name="comment-post"),
    
]
