from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/update/<slug:username>/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('accounts/profile/subscribe/<slug:username>/', views.SubscribeAPIView.as_view(), name='profile-subscribe'),
    path('accounts/profile/api/friend_requests/<slug:username>/', views.FriendRequestAPIView.as_view(), name='profile-requests'),
    path('accounts/profile/api/friend_requests/handler/<slug:username>/', views.FriendRequestHandlerAPIView.as_view(), name='profile-requests-handler'),
    path('accounts/profile/friend_requests/<slug:username>/', views.friend_requests_view, name='profile-friend-requests'),
    path('accounts/profile/posts/<slug:username>/', views.profile_posts_view, name='profile-posts'),
    path('accounts/profile/', views.profile_middleware, name='profile_middleware'),
]

