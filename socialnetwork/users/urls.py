from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/update/<slug:username>/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('accounts/profile/subscribe/<slug:username>/', views.SubscribeAPIView.as_view(), name='profile-subscribe'),
    path('accounts/profile/', views.profile_middleware, name='profile_middleware'),
]

