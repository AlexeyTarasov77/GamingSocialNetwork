from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("posts/", include("api.posts_api.urls", namespace="posts")),
    path("users/", include("api.users_api.urls", namespace="users")),
    path("search/", include("api.search_api.urls", namespace="search")),
]
