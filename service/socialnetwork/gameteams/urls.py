from django.urls import path, include
from . import views

app_name = 'gameteams'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('list/', views.TeamListView.as_view(), name='team_list'),
    path('create/', views.TeamCreateView.as_view(), name='team_create'),
    path('detail/<slug:slug>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('join/<slug:slug>/', views.TeamJoinView.as_view(), name='team_join'),
    path('join-requests/<slug:slug>/', views.TeamJoinRequestsView.as_view(), name='team_join_requests'),
    path('team-handle/<slug:slug>/', views.team_handle_view, name='team_handle'),
    path('team-leave/<slug:slug>/', views.leave_team_view, name='team_leave'),
    path('make-team-leader/<int:pk>/', views.make_team_leader_view, name='make_team_leader'),
    path('remove-team-member/<int:pk>/', views.remove_team_member_view, name='remove_team_member'),
    path('ads/create/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/list/', views.AdListView.as_view(), name='ad_list'),
    path('ads/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/<int:pk>/bookmark/', views.ad_bookmark_view, name='ad_bookmark'),
]
