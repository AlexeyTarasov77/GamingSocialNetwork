from core.HandleCache import use_cache
from django.core.cache import cache
from django.db import models
from django.db.models import Case, Count, Q, Value, When, QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from gameblog.redis_connection import r
from taggit.models import Tag
from .constants import CACHE_KEYS
from posts.models import Post


class PostListService:
    def __init__(
        self, user: User, content_type: Post.Type = Post.Type.POST, tag_slug: str = None
    ) -> None:
        self.user = user
        self.content_type = content_type
        self.tag_slug = tag_slug
        self.queryset: QuerySet[Post] = None
        self.cache_key = CACHE_KEYS["POSTS_LIST"].format(
            user_id=user.id, version=cache.get(CACHE_KEYS["POSTS_LIST_VERSION"], 0)
        )
        self.suggester = PostSuggestionService()

    def _filter_by_tag(self):
        tag = get_object_or_404(Tag, slug=self.tag_slug)
        self.queryset = self.queryset.filter(tags__in=[tag])

    @use_cache(5 * 60)
    def _fetch_posts(self):
        tag_slug = self.tag_slug
        content_type = self.content_type
        user = self.user
        self.queryset = (
            Post.published.annotate(
                count_likes=Count("liked"), count_comments=Count("comments")
            )
            .select_related("author")
            .order_by("-count_likes", "-count_comments")
        )
        if content_type and content_type in Post.Type.choices:
            self.queryset = self.queryset.filter(type=content_type)
        if user.is_authenticated:
            self.suggester.suggest_per_user(self.user, self.queryset)
        if tag_slug is not None:
            self._filter_by_tag(tag_slug)
        self.queryset = self.queryset.prefetch_related(
            "tags", "liked", "saved", "comments"
        )
        return self.queryset

    def execute(self) -> QuerySet[Post]:
        return self._fetch_posts()


class PostSuggestionService:
    def __init__(self) -> None:
        self.queryset: QuerySet[Post] = None

    def get_suggested_users(self, user):
        profile = user.profile
        suggested_authors = User.objects.filter(
            Q(id__in=profile.following.all()) | Q(id__in=profile.friends.all())
        )
        self.suggested_authors = suggested_authors
        return suggested_authors

    def _order_by_suggested_authors(self):
        suggested_authors_ids = [author.id for author in self.suggested_authors]
        return self.queryset.annotate(
            is_suggested_author=Case(
                When(author_id__in=suggested_authors_ids, then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField(),
            )
        ).order_by("-is_suggested_author")

    def _suggest_content(self, user):
        ids_to_exclude = set()
        for post in self.queryset:
            if r.sismember("post:%s:viewers" % post.id, user.id):
                ids_to_exclude.add(post.id)
        self.queryset = self.queryset.exclude(id__in=ids_to_exclude)
        suggested_authors = self.get_suggested_users(user)
        if suggested_authors:
            self._order_by_suggested_authors()

    def suggest_per_user(self, user, queryset):
        self.queryset = queryset
        self.queryset = self.queryset.exclude(author=user)
        if suggested := self._suggest_content(user):
            return suggested

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
