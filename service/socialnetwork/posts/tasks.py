from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .models import Post


@shared_task
def share_post_by_mail(
    user_id: int, post_id: int, cd: dict, post_url, new_post: bool = False
):
    user = get_object_or_404(get_user_model(), id=user_id)
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if new_post:
        subject = f"Пользователь {user} из списка ваших подписчиков опубликовал новый пост: {post.name}"
        message = f"Вы можете посмотреть его по ссылке: {post_url}\n\n"
        recipients = user.profile.followers.all().values_list("email", flat=True)
    else:
        recipients = [cd["to"]]
        subject = f"Пользователь: {user} поделился с вами постом: {post.name}, опубликованным - {post.author}"
        message = (
            f"Вы можете посмотреть пост - {post.name} по ссылке {post_url}\n\n"
            f"Комментарий пользователя {user}: {cd['notes']}"
        )

    send_mail(subject, message, None, recipients)


@shared_task
def recommend_posts_by_mail():
    two_days_ago = datetime.now() - timedelta(days=2)
    posts = (
        Post.published.filter(created_at__gte=two_days_ago)
        .annotate(
            count_likes=Count("liked"),
            count_comments=Count("comments"),
            count_saved=Count("saved"),
        )
        .order_by("-count_likes", "-count_comments", "-count_saved")[:3]
    )
    if posts:
        subject = "Рекомендации для вас"
        message_body = " ".join(
            [
                f"Пост No{i+1}: {post.name}\n{HttpRequest.build_absolute_uri(post.get_absolute_url())}\n\n"
                for i, post in enumerate(posts)
            ]
        )
        message = f"""
        Здесь {len(posts)} новых рекомендованных постов которые могут вас заинтересовать.
        {message_body}
        """
        users = get_user_model().objects.filter(email__isnull=False, is_active=True)
        send_mail(subject, message, None, [user.email for user in users])
