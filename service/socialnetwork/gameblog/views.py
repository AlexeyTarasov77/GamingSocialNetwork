import logging
import os
from datetime import timedelta
from typing import Any, Final

import requests
from actions.models import Action
from core.views import CatchExceptionMixin, set_logger
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.utils import timezone
from django.views import generic
from dotenv import load_dotenv
from posts.models import Post

from .models import Ad, BackgroundVideo

load_dotenv()
logger = logging.getLogger(__name__)
set_logger(logger)

count_users = get_user_model().objects.count()
# constants specifying the number of likes | comments required to get to recommends
# constants specifying the number of likes | comments required to get to recommends
TOTAL_LIKES_REQUIRED: Final[int] = count_users // 3
TOTAL_COMMENTS_REQUIRED: Final[int] = count_users // 4


class MainView(CatchExceptionMixin, generic.ListView):
    """View for main page"""

    template_name = "gameblog/index.html"
    context_object_name = "ads"

    def get_queryset(self) -> QuerySet[Ad]:
        """Getting ads from last 2 days"""
        two_days_ago = timezone.now() - timedelta(days=2)
        return Ad.objects.filter(time_create__gte=two_days_ago)

    def _get_last_actions(self):
        """Computing last users actions on the website"""
        try:
            actions = Action.objects.all()
            if actions:
                user = self.request.user
                if user.is_authenticated:
                    actions = actions.exclude(user=user)
                    following_ids = user.profile_following.values_list("id", flat=True)
                    if following_ids:
                        actions = actions.filter(user_id__in=following_ids)
                return actions.select_related("user", "user__profile").prefetch_related("target")[:10]
        except Exception as e:
            logger.exception(e)
            return []

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Adds to context last actions and recommended posts."""
        """Adds to context last actions and recommended posts."""
        context = super().get_context_data(**kwargs)
        context["last_actions"] = self._get_last_actions()
        context["recommended_posts"] = (
            Post.published.annotate(total_likes=Count("liked"), total_comments=Count("comments"))
            .filter(
                Q(total_likes__gte=TOTAL_LIKES_REQUIRED) | Q(total_comments__gte=TOTAL_COMMENTS_REQUIRED)
            )[:10]
            .select_related("author")
        )
        try:
            context["video_url"] = BackgroundVideo.objects.latest("pk")
        except ObjectDoesNotExist:
            context["video_url"] = ""
        return context


class GetNews(CatchExceptionMixin, generic.ListView):
    """Gets last game's news from Steam API"""

    template_name = "gameblog/news.html"
    context_object_name = "response"

    def get_queryset(self) -> QuerySet[Any]:
        game_id = self.kwargs.get("game_id")
        api_url = f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={game_id}&count=10&maxlength=0&format=json&feeds=steam_community_announcements"
        headers = {"Authorization": f'Bearer {os.getenv('STEAM_API_KEY')}'}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        logger.warning(f"GetNews error getting news from api. Status: {response.status_code}.")
        return []
