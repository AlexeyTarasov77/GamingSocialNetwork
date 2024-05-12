from django.urls import path, include
from . import views

app_name = 'gameteams'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('create/', views.TeamCreateView.as_view(), name='team_create'),
    path('ads/create/', views.AdCreateView.as_view(), name='ad_create'),
]
