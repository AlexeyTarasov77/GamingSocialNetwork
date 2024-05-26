from django.core.cache import cache
from django.db import models
from django.db.models import Case, Count, Q, Value, When, QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from gameblog.redis_connection import r
from taggit.models import Tag

from posts.models import Post
from posts.utils import get_from_cache_or_compute


class PostListService:
    def __init__(self, user: User,
                content_type: Post.Type = Post.Type.POST,
                tag_slug: str = None) -> None:
        self.user = user
        self.content_type = content_type
        self.tag_slug = tag_slug
        self.queryset: QuerySet[Post] = None
        self.cache_key = f"posts_feed_for_user_{self.user.id}_{cache.get("posts_feed_version", 0)}"
    
    def _get_suggested_authors(self):
        profile = self.user.profile
        suggested_authors = User.objects.filter(
            Q(id__in=profile.following.all())
            | Q(id__in=profile.friends.all())
        )
        return suggested_authors
    
    def _sort_by_suggested_authors(self, suggested_authors_ids):
        return self.queryset.annotate(
            is_suggested_author=Case(
                When(author_id__in=suggested_authors_ids, then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField(),
            )
        ).order_by("-is_suggested_author")
    
    def _suggest_content(self):

        for post in self.queryset:
            if r.sismember("post:%s:viewers" % post.id, self.user.id): 
                self.queryset = self.queryset.exclude(id=post.id)
        suggested_authors = self._get_suggested_authors()
        if suggested_authors:
            suggested_authors_ids = [author.id for author in suggested_authors]
            self._sort_by_suggested_authors(suggested_authors_ids)
            
    def _suggest_per_user(self):
        self.queryset = self.queryset.exclude(author_id=self.user.id)
        if suggested := self._suggest_content():
            self.queryset = suggested
            
    def _filter_by_tag(self):
        tag = get_object_or_404(Tag, slug=self.tag_slug)
        self.queryset = self.queryset.filter(tags__in=[tag])
        
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
            self._suggest_per_user()
        if tag_slug is not None:
            self._filter_by_tag(tag_slug)
        self.queryset = self.queryset.prefetch_related("tags", "liked", "saved", "comments")
        cache.set(self.cache_key, self.queryset, 360)
        return self.queryset
            
    def _fetch_posts_using_cache(self):
        return get_from_cache_or_compute(self.cache_key, self._fetch_posts)
        
    def execute(self) -> QuerySet[Post]:
        return self._fetch_posts_using_cache()
