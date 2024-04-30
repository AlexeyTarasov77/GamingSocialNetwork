from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('posts/', include('api.posts_api.urls', namespace='posts')),
]