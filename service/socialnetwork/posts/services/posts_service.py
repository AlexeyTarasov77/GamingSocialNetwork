from core.handle_cache import HandleCacheService
from core.redis_connection import r
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Case, Count, IntegerField, QuerySet, Value, When
from django.shortcuts import get_object_or_404
from taggit.models import Tag

from posts.models import Post

from .constants import CACHE_KEYS
from .m2m_toggle import ToggleLikeService, ToggleSaveService


def _invalidate_cache():
    HandleCacheService().invalidate_cache_version(CACHE_KEYS["POSTS_DETAIL_VERSION"])
    HandleCacheService().invalidate_cache_version(CACHE_KEYS["POSTS_LIST_VERSION"])


class PostsService:
    """
    Service for working with Post objects.
    """

    @staticmethod
    def fetch_post(**params) -> Post:
        """
        Fetch a post by given parameters.

        :param params: Parameters for filtering Post objects.
        :return: Fetched Post object.
        """
        post = get_object_or_404(
            Post.published.select_related("author").prefetch_related(
                "tags", "liked", "saved"
            ),
            **params,
        )
        return post

    @staticmethod
    def is_post_author(obj: Post, user_id: int) -> bool:
        """Check if a post's author is a user.

        :param obj: Post object.
        :param user_id: User ID.
        :return: True if the author is a user, False otherwise.
        """
        return obj.author_id == user_id

    @staticmethod
    def order_by_popularity(posts: QuerySet[Post]) -> QuerySet[Post]:
        """
        Order posts by popularity.

        :param posts: QuerySet of Post objects.
        :return: QuerySet of ordered Post objects.
        """
        return posts.annotate(
            count_likes=Count("liked"),
            count_comments=Count("comments"),
            count_saved=Count("saved"),
        ).order_by("-count_likes", "-count_comments", "-count_saved")

    @staticmethod
    def order_by_authors(
        posts: QuerySet[Post], authors_ids: list[int]
    ) -> QuerySet[Post]:
        """
        Order posts by authors.

        :param posts: QuerySet of Post objects.
        :param authors_ids: List of author IDs.
        :return: QuerySet of ordered Post objects.
        """
        return posts.annotate(
            is_suggested_author=Case(
                When(author_id__in=authors_ids, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by("-is_suggested_author")

    @staticmethod
    def exclude_viewed(posts: QuerySet[Post], user: AbstractBaseUser) -> QuerySet[Post]:
        """
        Exclude posts viewed by a user.

        :param posts: QuerySet of Post objects.
        :param user: User object.
        :return: QuerySet of Post objects excluding viewed posts.
        """
        ids_to_exclude = set()
        for post in posts:
            if r.sismember("post:%s:viewers" % post.id, user.id):
                ids_to_exclude.add(post.id)
        return posts.exclude(id__in=ids_to_exclude)

    @staticmethod
    def suggest_by_tags(post: Post, max_count=4) -> QuerySet[Post]:
        """
        Suggest posts by tags.

        :param post: Post object.
        :param max_count: Maximum count of suggested posts.
        :return: QuerySet of suggested Post objects.
        """
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

    @classmethod
    def get_most_popular(cls, max_count=5, **filters) -> QuerySet[Post]:
        """
        Get most popular posts.

        :param max_count: Maximum count of posts.
        :param filters: Filters for Post objects.
        :return: QuerySet of most popular Post objects.
        """
        posts = Post.published.all()
        if filters:
            posts = posts.filter(**filters)
        return cls.order_by_popularity(posts)[:max_count]

    @staticmethod
    def filter_by_type(posts: QuerySet[Post], post_type: str) -> QuerySet[Post]:
        """
        Filter posts by type.

        :param posts: QuerySet of Post objects.
        :param post_type: Type of posts.
        :return: QuerySet of filtered Post objects.
        """
        if post_type in Post.Type.choices:
            return posts.filter(type=post_type)
        return posts

    @staticmethod
    def filter_by_tag(posts: QuerySet[Post], tag_slug: str) -> QuerySet[Post]:
        """
        Filter posts by tag slug.

        :param posts: QuerySet of Post objects.
        :param tag_slug: Slug of tag.
        :return: QuerySet of filtered Post objects.
        """
        tag = get_object_or_404(Tag, slug=tag_slug)
        return posts.filter(tags=tag)

    @staticmethod
    def like_post(obj: Post, user) -> Post:
        """
        Like a post.

        :param obj: Post object.
        :param user: User object.
        :return: Liked Post object.
        """
        _invalidate_cache()
        return ToggleLikeService(obj, user).execute()

    @staticmethod
    def save_post(obj: Post, user) -> Post:
        """
        Save a post.

        :param obj: Post object.
        :param user: User object.
        :return: Saved Post object.
        """
        _invalidate_cache()
        return ToggleSaveService(obj, user).execute()
