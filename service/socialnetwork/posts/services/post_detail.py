from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from posts.models import Post
from posts.utils import get_from_cache_or_compute


class PostDetailService:
    def __init__(self, user: User, post_id: int) -> None:
        self.user = user
        self.post_id = post_id
        self.post = None
        self.cache_key = f"posts_detail_{self.post_id}"
    
    def _fetch_post(self):
        self.post = get_object_or_404(
            Post.objects.select_related("author").prefetch_related(
                "tags", "liked", "saved", "comments"
            ),
            pk=self.post_id,
        )
        cache.set(self.cache_key, self.post, 60 * 15)
        return self.post
    
    def _fetch_post_using_cache(self):
        return get_from_cache_or_compute(self.cache_key, self._fetch_post)
    
    def execute(self) -> Post:
        return self._fetch_post_using_cache()