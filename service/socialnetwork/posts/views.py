from typing import Any

from .services.posts_service import PostsService
from core.handle_cache import HandleCacheService
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.core.cache import cache
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from core import views
from .services.constants import CACHE_KEYS
from . import forms, tasks
from .mixins import ListPostsQuerySetMixin
from core.mixins import ObjectViewsMixin
from .models import Post
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

views.set_logger(logger)


class ListPosts(views.BaseView, ListPostsQuerySetMixin, generic.ListView):
    template_name = "posts/list.html"
    context_object_name = "posts_list"
    paginate_by = 10


class DetailPost(ObjectViewsMixin, generic.DetailView):
    template_name = "posts/detail.html"
    context_object_name = "post"
    redis_key_prefix = "posts"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        post_id = self.kwargs.get("post_id")
        cache_key = CACHE_KEYS["POSTS_DETAIL"].format(
            post_id=post_id, version=cache.get(CACHE_KEYS["POSTS_DETAIL_VERSION"], 0)
        )
        cached_fetch_post = HandleCacheService.use_cache(cache_key, 60 * 15)(PostsService.fetch_post)
        post = cached_fetch_post(id=post_id)
        return post

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context["is_owner"] = PostsService.is_post_author(post, self.request.user.id)
        context["form"] = forms.CommentForm
        context["filtered_comments"] = (
            post.comments.filter(is_active=True)
            .select_related("author__profile")
            .prefetch_related("liked")
        )
        context["recommended_posts"] = PostsService.suggest_by_tags(post)
        return context


class DeletePost(generic.DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("posts:list-posts")
    context_object_name = "post"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Пост успешно удален")
        return super().form_valid(form)


class UpdatePost(generic.UpdateView):
    template_name = "posts/update.html"
    model = Post
    form_class = forms.UpdatePostForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.warning(self.request, "Пост успешно обновлен")
        HandleCacheService().invalidate_cache_version(CACHE_KEYS["POST_DETAIL_VERSION"])
        return super().form_valid(form)


class CreatePost(LoginRequiredMixin, generic.CreateView):
    template_name = "posts/create.html"
    form_class = forms.CreatePostForm
    queryset = Post.objects.select_related("author")

    def form_valid(self, form):
        post = form.save(commit=False)
        user_id = self.request.user.id
        post.author_id = user_id
        post.save()
        form.save_m2m()
        tasks.share_post_by_mail.delay(
            user_id,
            post.id,
            None,
            self.request.build_absolute_uri(post.get_absolute_url()),
            True,
        )
        HandleCacheService().invalidate_cache_version(CACHE_KEYS["POSTS_LIST_VERSION"])
        return redirect(post.get_absolute_url())


# Share post by email address
@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = forms.ShareForm()
    if request.method == "POST":
        form = forms.ShareForm(request.POST)
        if form.is_valid():
            tasks.share_post_by_mail.delay(
                request.user.id,
                post_id,
                form.cleaned_data,
                request.build_absolute_uri(post.get_absolute_url()),
            )
            return HttpResponse()
    return render(request, "posts/share_post.html", locals())
