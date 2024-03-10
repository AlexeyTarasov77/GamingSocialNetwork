from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Post
from django.contrib.auth import get_user_model
from django.conf import settings

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