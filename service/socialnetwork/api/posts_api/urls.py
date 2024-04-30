from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.PostsViewSet, basename='posts')

app_name = 'posts'

urlpatterns = [
    path('v1/', include(router.urls)),
]
