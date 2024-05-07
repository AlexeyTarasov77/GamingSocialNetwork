from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.SearchAPIView.as_view(), name='search'),
    path('credentials/', views.SearchAPICredetials.as_view(), name='credentials'),
]