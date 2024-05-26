from typing import Any

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.db.models import Case, Count, Q, Value, When
from django.shortcuts import get_object_or_404
from gameblog.redis_connection import r
from taggit.models import Tag

from .models import Post
from .services import PostListService

posts_feed_version_cache_key = "posts_feed_version"

User = get_user_model()

class ListPostsQuerySetMixin:
    # def __suggest_posts_for_user(self, user, queryset):
    #     profile = user.profile
    #     for post in queryset:
    #         if r.sismember("post:%s:viewers" % post.id, user.id): 
    #             queryset = queryset.exclude(id=post.id)
    #     suggested_authors = User.objects.filter(
    #         Q(id__in=profile.following.all())
    #         | Q(id__in=profile.friends.all())
    #     )
    #     if suggested_authors:
    #         suggested_authors_ids = [author.id for author in suggested_authors]

    #         return queryset.annotate(
    #             is_suggested_author=Case(
    #                 When(author_id__in=suggested_authors_ids, then=Value(1)),
    #                 default=Value(0),
    #                 output_field=models.IntegerField(),
    #             )
    #         ).order_by("-is_suggested_author")
    def get_queryset(self):
        post_type = self.request.GET.get("type") or Post.Type.POST
        user = self.request.user
        tag_slug = self.kwargs.get("tag_slug")
        queryset = PostListService(user, post_type, tag_slug).execute()
        return queryset
        # request = self.request
        # user = request.user
        # cache_key = f"posts_feed_for_user_{user.id}_{cache.get("posts_feed_version", 0)}"
        # data = cache.get(cache_key)
        # if data:
        #     return data
        # queryset = (
        #     Post.published.annotate(
        #         count_likes=Count("liked"), count_comments=Count("comments")
        #     )
        #     .select_related("author")
        #     .order_by("-count_likes", "-count_comments")
        # )
        # post_type = request.GET.get("type") or Post.Type.POST
        # if post_type and post_type in Post.Type.choices:
        #     queryset = queryset.filter(type=post_type)
        # if user.is_authenticated:
        #     queryset = queryset.exclude(author_id=user.id)
        #     suggested_posts = self.__suggest_posts_for_user(user, queryset)
        #     if suggested_posts:
        #         queryset = suggested_posts
        # tag_slug = self.kwargs.get("tag_slug")
        # if tag_slug is not None:
        #     tag = get_object_or_404(Tag, slug=tag_slug)
        #     queryset = queryset.filter(tags__in=[tag])
        # queryset = queryset.prefetch_related("tags", "liked", "saved", "comments")
        # cache.set(cache_key, queryset, 360)
        # return queryset
    

class ObjectViewsMixin:
    redis_key_prefix = None
    def get_or_update_object_views(self, viewers_key, views_key):
        user_id = str(self.request.user.id)
        viewed_users_ids = r.smembers(viewers_key) or []
        if not user_id in viewed_users_ids:
            r.sadd(viewers_key, user_id)
            total_views = r.incr(views_key)
        else:
            total_views = r.get(views_key)
        return total_views
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["views_count"] = self.get_or_update_object_views(f"{self.redis_key_prefix}:{self.object.id}:viewers", f"{self.redis_key_prefix}:{self.object.id}:views")
        return context