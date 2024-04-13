from django.urls import include, path

from . import views

app_name = "users"

prefix = "accounts/profile"

urlpatterns = [
    path(
        f"{prefix}/<slug:username>/", views.ProfileView.as_view(), name="profile"
    ),
    path(
        f"{prefix}/update/<slug:username>/",
        views.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path(
        f"{prefix}/subscribe/<slug:username>/",
        views.SubscribeAPIView.as_view(),
        name="profile-subscribe",
    ),
    path(
        f"{prefix}/api/friend_requests/<slug:username>/",
        views.FriendRequestAPIView.as_view(),
        name="profile-requests",
    ),
    path(
        f"{prefix}/api/friend_requests/handler/<slug:username>/",
        views.FriendRequestHandlerAPIView.as_view(),
        name="profile-requests-handler",
    ),
    path(
        f"{prefix}/friend_requests/<slug:username>/",
        views.friend_requests_view,
        name="profile-friend-requests",
    ),
    path(
        f"{prefix}/posts/<slug:username>/", views.my_posts_view, name="my_posts"
    ),
    path(
        f"{prefix}/orders/<slug:username>/", views.my_orders_view, name="my_orders"
    ),
    path(f"{prefix}/", views.profile_middleware, name="profile_middleware"),
]
