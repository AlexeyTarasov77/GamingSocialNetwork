from typing import Any

from . import services
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models.base import Model 
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from . import forms, tasks
from .mixins import (
    ListPostsQuerySetMixin,
    ObjectViewsMixin,
    posts_feed_version_cache_key,
)
from .models import Post

User = get_user_model()


# Create your views here.
class ListPosts(ListPostsQuerySetMixin, generic.ListView):
    template_name = "posts/list.html"
    context_object_name = "posts_list"
    paginate_by = 10


class DetailPost(ObjectViewsMixin, generic.DetailView):
    template_name = "posts/detail.html"
    context_object_name = "post"
    redis_key_prefix = "posts"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return services.PostDetailService(
            self.request.user, self.kwargs.get("post_id")
        ).execute()

    def _get_simillar_posts(self):
        post = self.object
        return services.SimillarPostsByTagService(post).execute()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context["is_owner"] = services.CheckIsAuthorService(
            post, self.request.user, "author"
        ).execute()
        context["form"] = forms.CommentForm
        context["filtered_comments"] = (
            post.comments.filter(is_active=True)
            .select_related("author__profile")
            .prefetch_related("liked")
        )
        context["recommended_posts"] = self._get_simillar_posts()
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
        cache.set(
            posts_feed_version_cache_key, cache.get(posts_feed_version_cache_key, 0) + 1
        )
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
