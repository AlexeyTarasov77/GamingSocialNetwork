from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Черновик"
        PUBLISHED = "PB", "Опубликовано"

    name = models.CharField(
        verbose_name="Заголовок поста", max_length=100, db_index=True
    )
    content = models.TextField(verbose_name="Контент")
    time_create = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    time_update = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    time_publish = models.DateTimeField(
        verbose_name="Дата публикации", default=timezone.now
    )
    status = models.CharField(
        verbose_name="Статус",
        choices=Status.choices,
        default=Status.PUBLISHED,
        max_length=2,
        db_index=True,
    )
    photo = models.ImageField(
        verbose_name="Фото", blank=True, upload_to="photos/posts/", null=True
    )
    saved = models.ManyToManyField(
        get_user_model(),
        verbose_name="Сохраненные",
        related_name="saved_posts",
        blank=True,
    )
    liked = models.ManyToManyField(
        get_user_model(), verbose_name="Лайки", related_name="liked_posts", blank=True
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    tags = TaggableManager(blank=True, verbose_name="Теги")
    published = PublishedManager()
    objects = models.Manager()  # The default manager

    class Meta:
        ordering = ["-time_create"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.name
    
    def tag_list(self):
        return [t.name for t in self.tags.all()]
    
    def is_published(self):
        return self.status == Post.Status.PUBLISHED

    @property
    def num_likes(self):
        return self.liked.count()

    @property
    def num_comments(self):
        return self.comments.count()

    def get_absolute_url(self):
        return reverse("posts:detail-post", kwargs={"post_id": self.pk})


class Comment(MPTTModel):
    class CommentManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="Пост", related_name="comments"
    )
    author = models.ForeignKey(
        get_user_model(), verbose_name="Автор", on_delete=models.CASCADE
    )
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    is_active = models.BooleanField(default=True)
    liked = models.ManyToManyField(
        get_user_model(),
        verbose_name="Лайки",
        related_name="liked_comments",
        blank=True
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="comment_parent",
        verbose_name="Родительский комментарий",
    )
    objects = models.Manager
    active = CommentManager()

    class MPTTMeta:
        order_insertion_by = ["-time_create"]

    class Meta:
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create", "parent"])]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return f"{self.author}: {self.content}"

    @property
    def get_avatar(self):
        if self.author:
            return self.author.profile.image
        return f"https://w7.pngwing.com/pngs/686/219/png-transparent-youtube-user-computer-icons-information-youtube-hand-silhouette-avatar.png"
