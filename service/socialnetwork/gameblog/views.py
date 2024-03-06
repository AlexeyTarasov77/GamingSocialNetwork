from datetime import timedelta
from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.views import generic
from .models import Ad, BackgroundVideo
from posts.models import Post
from django.db.models import Count, Q
import requests
from decouple import config
from django.core.exceptions import ObjectDoesNotExist



total_likes_required = 20
total_comments_required = 10

# Create your views here.
class MainView(generic.ListView):
    template_name = 'gameblog/index.html'
    context_object_name = 'ads'
    
    def get_queryset(self) -> QuerySet[Any]:
        two_days_ago = timezone.now() - timedelta(days=2)
        return Ad.objects.filter(time_create__gte = two_days_ago)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['recommended_posts'] = Post.published.annotate(
            total_likes = Count('liked'),
            total_comments=Count('comment_post')
        ).filter(Q(total_likes__gte=total_likes_required) | Q(total_comments__gte=total_comments_required))[:10]
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
         