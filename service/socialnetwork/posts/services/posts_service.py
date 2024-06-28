from core.handle_cache import HandleCacheService
from core.redis_connection import r
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Case, Count, IntegerField, Q, QuerySet, Value, When
from django.shortcuts import get_object_or_404
from posts.models import Post
from taggit.models import Tag
from .m2m_toggle import ToggleLikeService, ToggleSaveService
from .constants import CACHE_KEYS, TOTAL_COMMENTS_REQUIRED, TOTAL_LIKES_REQUIRED


def _invalidate_cache():
    HandleCacheService().invalidate_cache_version(CACHE_KEYS["POSTS_DETAIL_VERSION"])
    HandleCacheService().invalidate_cache_version(CACHE_KEYS["POSTS_LIST_VERSION"])


class PostsService:

    @staticmethod
    def fetch_post(**params):
        print('ATTENTION ---- - -- - - called fetch_post')
        post = get_object_or_404(
            Post.objects.select_related("author").prefetch_related("tags", "liked", "saved"),
            **params
        )
        return post

    @staticmethod
    def is_post_author(obj, user_id):
        return obj.author_id == user_id

    @staticmethod
    def order_by_popularity(posts: QuerySet[Post]):
        return posts.annotate(
            count_likes=Count("liked"), count_comments=Count("comments")
        ).order_by("-count_likes", "-count_comments")

    @staticmethod
    def order_by_authors(
        posts: QuerySet[Post], authors_ids: list[int]
    ) -> QuerySet[Post]:
        return posts.annotate(
            is_suggested_author=Case(
                When(author_id__in=authors_ids, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by("-is_suggested_author")

    @staticmethod
    def exclude_viewed(posts: QuerySet[Post], user: AbstractBaseUser) -> QuerySet[Post]:
        ids_to_exclude = set()
        for post in posts:
            if r.sismember("post:%s:viewers" % post.id, user.id):
                ids_to_exclude.add(post.id)
        return posts.exclude(id__in=ids_to_exclude)

    @staticmethod
    def suggest_by_tags(post, max_count=4):
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = (
            Post.published.filter(tags__in=post_tags_ids)
            .exclude(id=post.id)
            .annotate(same_tags=Count("tags"))
            .select_related("author")
            .prefetch_related("tags", "liked", "saved", "comments")
            .order_by("-same_tags")[:max_count]
        )
        return similar_posts

    @staticmethod
    def get_recommended():
        return Post.published.annotate(
            total_likes=Count("liked"), total_comments=Count("comments")
        ).filter(
            Q(total_likes__gte=TOTAL_LIKES_REQUIRED)
            | Q(total_comments__gte=TOTAL_COMMENTS_REQUIRED)
        )

    @staticmethod
    def filter_by_type(posts: QuerySet[Post], post_type: str) -> QuerySet[Post]:
        if post_type in Post.Type.choices:
            return posts.filter(type=post_type)
        return posts

    @staticmethod
    def filter_by_tag(posts: QuerySet[Post], tag_slug: str) -> QuerySet[Post]:
        tag = get_object_or_404(Tag, slug=tag_slug)
        return posts.filter(tags=tag)

    @staticmethod
    def like_post(obj, user):
        _invalidate_cache()
        return ToggleLikeService(obj, user).execute()

    @staticmethod
    def save_post(obj, user):
        _invalidate_cache()
        return ToggleSaveService(obj, user).execute()
