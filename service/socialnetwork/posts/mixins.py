from django.contrib.auth import get_user_model
from users.services.users_service import UsersService

from .models import Post
from .services.posts_service import PostsService
from .services.constants import CACHE_KEYS
from core.handle_cache import HandleCacheService
from django.core.cache import cache

User = get_user_model()


class ListPostsQuerySetMixin:
    def get_queryset(self):
        post_type = self.request.GET.get("type") or Post.Type.POST
        user = self.request.user
        tag_slug = self.kwargs.get("tag_slug")
        cache_key = CACHE_KEYS["POSTS_LIST"].format(
            post_type=post_type, tag_slug=tag_slug,
            user_id=user.id,
            version=cache.get(CACHE_KEYS["POSTS_LIST_VERSION"], 0)
        )

        @HandleCacheService.use_cache(cache_key, 60 * 15)
        def posts_queryset():
            queryset = PostsService.filter_by_type(
                PostsService.order_by_popularity(Post.published.all()),
                post_type,
            )
            if tag_slug is not None:
                queryset = PostsService.filter_by_tag(queryset, tag_slug)
            if user.is_authenticated:
                authors_ids = [
                    author.id for author in UsersService.get_suggested_users_per_user(user)
                ]
                queryset = PostsService.order_by_authors(
                    PostsService.exclude_viewed(queryset, user),
                    authors_ids,
                )
            return queryset.select_related("author").prefetch_related(
                "tags", "liked", "saved", "comments"
            )
        return posts_queryset()
