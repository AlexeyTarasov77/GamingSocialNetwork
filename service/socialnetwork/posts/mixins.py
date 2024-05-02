from django.db.models import Case, Count, Q, Value, When
from .models import Post
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from taggit.models import Tag
import redis
from django.conf import settings


# r = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB,
#     decode_responses=True,
# )

User = get_user_model()

class ListPostsQuerySetMixin:
    def __suggest_posts_for_user(self, user, queryset):
        profile = user.profile
        queryset = queryset.exclude(author_id=user.id)
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
        queryset = (
            Post.published.annotate(
                count_likes=Count("liked"), count_comments=Count("comments")
            )
            .select_related("author")
            .order_by("-count_likes", "-count_comments")
        )
        user = self.request.user
        if user.is_authenticated:
            queryset = self.__suggest_posts_for_user(user, queryset)
        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug is not None:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        return queryset.prefetch_related("tags", "liked", "saved", "comments")