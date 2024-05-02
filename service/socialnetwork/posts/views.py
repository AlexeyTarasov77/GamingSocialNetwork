from typing import Any

import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .mixins import ListPostsQuerySetMixin
from . import forms, tasks
from .models import Post

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)

User = get_user_model()


# Create your views here.
class ListPosts(ListPostsQuerySetMixin, generic.ListView):
    template_name = "posts/list.html"
    context_object_name = "posts_list"
    paginate_by = 10
    


class DetailPost(generic.DetailView):
    template_name = "posts/detail.html"
    context_object_name = "post"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(
            Post.objects.select_related("author").prefetch_related("tags"),
            pk=self.kwargs.get("post_id"),
        )

    def __get_simillar_posts(self):
        post = self.object
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = (
            Post.published.filter(tags__in=post_tags_ids)
            .exclude(id=post.id)
            .annotate(same_tags=Count("tags"))
            .order_by("-same_tags", "-time_publish")[:4]
        )
        return similar_posts

    def __incr_views(self):
        post = self.object
        user_id = str(self.request.user.id)
        viewed_users_ids = r.smembers("post:%s:viewers" % post.id) or []
        if not user_id in viewed_users_ids:
            r.sadd("post:%s:viewers" % post.id, user_id)
            total_views = r.incr("post:%s:views" % post.id)
        else:
            total_views = r.get("post:%s:views" % post.id)
        return total_views

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context["is_owner"] = True if self.request.user == post.author else False
        context["form"] = forms.CommentForm
        context["filtered_comments"] = post.comments.filter(is_active=True)
        context["recommended_posts"] = self.__get_simillar_posts()
        total_views = self.__incr_views()
        context["views_count"] = total_views
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


class AddPost(LoginRequiredMixin, generic.CreateView):
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
