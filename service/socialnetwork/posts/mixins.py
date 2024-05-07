from django.db.models import Case, Count, Q, Value, When
from .models import Post
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from taggit.models import Tag

posts_feed_version_cache_key = "posts_feed_version"

User = get_user_model()

class ListPostsQuerySetMixin:
    def __suggest_posts_for_user(self, user, queryset):
        profile = user.profile
        from .views import r
        for post in queryset:
            if r.sismember("post:%s:viewers" % post.id, user.id): 
                queryset = queryset.exclude(id=post.id)
        suggested_authors = User.objects.filter(
            Q(id__in=profile.following.all())
            | Q(id__in=profile.friends.all())
        )
        if suggested_authors:
            suggested_authors_ids = [author.id for author in suggested_authors]

            return queryset.annotate(
                is_suggested_author=Case(
                    When(author_id__in=suggested_authors_ids, then=Value(1)),
                    default=Value(0),
                    output_field=models.IntegerField(),
                )
            ).order_by("-is_suggested_author")
    def get_queryset(self):
        request = self.request
        user = request.user
        cache_key = f"posts_feed_for_user_{user.id}_{cache.get("posts_feed_version", 0)}"
        data = cache.get(cache_key)
        if data:
            return data
        queryset = (
            Post.published.annotate(
                count_likes=Count("liked"), count_comments=Count("comments")
            )
            .select_related("author")
            .order_by("-count_likes", "-count_comments")
        )
        post_type = request.GET.get("type") or Post.Type.POST
        if post_type and post_type in Post.Type.choices:
            queryset = queryset.filter(type=post_type)
        if user.is_authenticated:
            queryset = queryset.exclude(author_id=user.id)
            suggested_posts = self.__suggest_posts_for_user(user, queryset)
            if suggested_posts:
                queryset = suggested_posts
        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug is not None:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        queryset = queryset.prefetch_related("tags", "liked", "saved", "comments")
        cache.set(cache_key, queryset, 360)
        return queryset