from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .models import Post


@shared_task
def share_post_by_mail(user_id: int, post_id: int, cd: dict, post_url):
    user = get_object_or_404(get_user_model(), id=user_id)
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    cd["username"] = user.username
    cd["email"] = user.email
    subject = f"User: {cd['username']} recommends you read: post - {post.name}, posted by {post.author}"
    message = (
        f"Read {post.name} at {post_url}\n\n"
        f"{cd['username']}'s comment: {cd['notes']}"
    )
    send_mail(subject, message, None, [cd["to"]])


@shared_task
def recommend_posts_by_mail():
    two_days_ago = datetime.now() - timedelta(days=2)
    posts = (
        Post.published.filter(created_at__gte=two_days_ago)
        .annotate(
            count_likes=Count("liked"),
            count_comments=Count("comment_post"),
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
