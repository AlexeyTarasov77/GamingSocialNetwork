from datetime import timedelta
from typing import Any, Final

import requests
from actions.models import Action
from decouple import config
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from posts.models import Post

from .models import Ad, BackgroundVideo

count_users = get_user_model().objects.count()
TOTAL_LIKES_REQUIRED: Final[int] = count_users // 3
TOTAL_COMMENTS_REQUIRED: Final[int] = count_users // 4

# Create your views here.
class MainView(generic.ListView):
    template_name = 'gameblog/index.html'
    context_object_name = 'ads'
    
    def get_queryset(self) -> QuerySet[Any]:
        two_days_ago = timezone.now() - timedelta(days=2)
        return Ad.objects.filter(time_create__gte = two_days_ago)
    
    def __get_last_actions(self):
        print(self.request.META.get("REMOTE_ADDR"))
        user = self.request.user
        actions = Action.objects.all()
        if user.is_authenticated:
            actions = actions.exclude(user=user)
            following_ids = user.profile_following.values_list('id', flat=True)
            if following_ids:
                actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
        return actions
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["last_actions"] = self.__get_last_actions()
        context['recommended_posts'] = Post.published.annotate(
            total_likes = Count('liked'),
            total_comments=Count('comments')
        ) \
        .filter(Q(total_likes__gte=TOTAL_LIKES_REQUIRED) | Q(total_comments__gte=TOTAL_COMMENTS_REQUIRED))[:10] \
        .select_related('author')
        try:
            context['video_url'] = BackgroundVideo.objects.latest('pk')
        except ObjectDoesNotExist:
            context['video_url'] = ""
        return context
    
    
class GetNews(generic.ListView):
    template_name = 'gameblog/news.html'
    context_object_name = 'response'
    def get_queryset(self) -> QuerySet[Any]:
        headers = {'Authorization': f'Bearer {config('STEAM_API_KEY')}'}
        response = requests.get(f'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={self.kwargs.get('game_id')}&count=10&maxlength=0&format=json&feeds=steam_community_announcements', headers=headers)
        if response.status_code == 200:
            return response.json()
         
