from django.urls import path, include
from . import views

app_name = 'gameblog'

urlpatterns = [
    path("", views.MainView.as_view(), name='main'),
    path("gameblog/get_news/<int:game_id>/", views.GetNews.as_view(), name='news'), 
    # path('settings/', SettingsView.as_view(), name = 'settings')
]