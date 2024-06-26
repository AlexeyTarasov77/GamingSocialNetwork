from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from .services.posts_service import PostsService

from .models import Post


@shared_task
def share_post_by_mail(
    user_id: int,
    post_id: int,
    cd: dict,
    post_url: str,
    new_post: bool = False
) -> None:
    """
    Share a post by email.

    Args:
        user_id (int): The ID of the user.
        post_id (int): The ID of the post.
        cd (dict): The comment data.
        post_url (str): The URL of the post.
        new_post (bool, optional): Whether it is a new post. Defaults to False.
    """
    # Get the user and post objects
    user = get_object_or_404(get_user_model(), id=user_id)
    post = get_object_or_404(
        Post.published.select_related("author"), id=post_id
    )

    # If it is a new post, set recipients to all followers
    if new_post:
        subject = (
            f"Пользователь {user} из списка ваших подписчиков "
            f"опубликовал новый пост: {post.title}"
        )
        message = f"Вы можете посмотреть его по ссылке: {post_url}\n\n"
        recipients = user.profile.followers.all().values_list(
            "email", flat=True
        )
    else:
        recipients = [cd["to"]]
        subject = (
            f"Пользователь: {user} поделился с вами постом: "
            f"{post.title}, опубликованным - {post.author}"
        )
        message = (
            f"Вы можете посмотреть пост - {post.title} по ссылке {post_url}\n\n"
            f"Комментарий пользователя {user}: {cd['notes']}"
        )

    # Send the email
    send_mail(subject, message, None, recipients)


@shared_task
def recommend_posts_by_mail() -> None:
    """
    Asynchronously sends email recommendations to active users who have
    non-null email addresses. The recommended posts are the top 3 most popular
    (based on likes, comments, and saves) published posts within the last 2 days.
    """
    # Get the 3 most popular posts within the last 2 days
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

    # If there are recommended posts, send emails
    if posts:
        # Set email subject and body
        subject = "Рекомендации для вас"
        message_body = " ".join(
            [
                f"Пост No{i+1}: {post.title}\n{HttpRequest.build_absolute_uri(post.get_absolute_url())}\n\n"  # noqa: E501
                for i, post in enumerate(posts)
            ]
        )
        message = f"""
        Здесь {len(posts)} новых рекомендованных постов которые могут вас заинтересовать.
        {message_body}
        """

        # Get active users with non-null email addresses
        users = get_user_model().objects.filter(
            email__isnull=False, is_active=True
        )

        # Send email to each user
        send_mail(subject, message, None, [user.email for user in users])
