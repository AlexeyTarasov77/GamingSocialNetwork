from .PostList import PostListService, PostSuggestionService
from .m2m_toggle import ToggleLikeService, ToggleSaveService
from .PostDetail import PostDetailService, CheckIsAuthorService
from posts.models import Post
from core.HandleCache import HandleCacheService
from .constants import CACHE_KEYS

def _invalidate_cache():
    HandleCacheService().invalidate_cache_version(CACHE_KEYS["POSTS_DETAIL_VERSION"])
    HandleCacheService().invalidate_cache_version(CACHE_KEYS["POSTS_LIST_VERSION"])

class PostService: 
    @staticmethod
    def like(post, user):
        _invalidate_cache()
        return ToggleLikeService(post, user).execute()
    @staticmethod    
    def save(post, user):
        _invalidate_cache()
        return ToggleSaveService(post, user).execute()
    @staticmethod    
    def list_posts(user, ct=Post.Type.POST, tag_slug=None):
        print(user, ct, tag_slug)
        return PostListService(user, ct, tag_slug).execute()
    @staticmethod    
    def post_detail(user, post_id):
        return PostDetailService(user, post_id).execute()
    @staticmethod    
    def is_post_author(obj, user):
        return CheckIsAuthorService(obj, user, "author").execute()
    @staticmethod    
    def simillar_posts_by_tag(post):
        return PostSuggestionService.suggest_by_tags(post)