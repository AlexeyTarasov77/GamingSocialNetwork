from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/profile/<slug:username>/', views.ProfileView.as_view(), name='profile')
]
