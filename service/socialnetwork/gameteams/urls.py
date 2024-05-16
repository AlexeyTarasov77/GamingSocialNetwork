from django.urls import path, include
from . import views

app_name = 'gameteams'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('list/', views.TeamListView.as_view(), name='team_list'),
    path('create/', views.TeamCreateView.as_view(), name='team_create'),
    path('detail/<slug:slug>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('ads/create/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/list/', views.AdListView.as_view(), name='ad_list'),
]
