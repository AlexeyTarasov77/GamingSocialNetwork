from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Model
from posts.models import Post
from core.HandleCache import use_cache
from .constants import CACHE_KEYS


class PostDetailService:
    def __init__(self, user: User, post_id: int) -> None:
        self.user = user
        self.post_id = post_id
        self.post = None
        self.cache_key = CACHE_KEYS["POSTS_DETAIL"] \
            .format(post_id=post_id, version=cache.get(CACHE_KEYS["POSTS_DETAIL_VERSION"], 0))
    
    @use_cache(60*15)
    def _fetch_post(self):
        self.post = get_object_or_404(
            Post.objects.select_related("author").prefetch_related(
                "tags", "liked", "saved", "comments"
            ),
            pk=self.post_id,
        )
        return self.post
    
    def execute(self) -> Post:
        return self._fetch_post()
    
class CheckIsAuthorService:
    def __init__(self, obj: Model, user: User, obj_owner_field_name: str) -> None:
        self.user = user
        self.object_author = getattr(obj, obj_owner_field_name)
        
    def _is_author(self):
        return self.object_author == self.user
    
    def execute(self) -> bool:
        return self._is_author()