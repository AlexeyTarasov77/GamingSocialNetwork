from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from django.utils.translation import gettext as _
from django.conf import settings


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    like_field = "liked"

    class Status(models.TextChoices):
        DRAFT = "DF", _("Черновик")
        PUBLISHED = "PB", _("Опубликовано")

    class Type(models.TextChoices):
        NEWS = "NW", _("Новость")
        ARTICLE = "AR", _("Статья")
        POST = "PS", _("Пост")

    title = models.CharField(
        verbose_name=_("Заголовок поста"), max_length=100, db_index=True
    )
    content = models.TextField(verbose_name=_("Контент"))
    time_create = models.DateTimeField(
        verbose_name=_("Дата создания"), auto_now_add=True
    )
    time_update = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now=True)
    time_publish = models.DateTimeField(
        verbose_name=_("Дата публикации"), default=timezone.now
    )
    status = models.CharField(
        verbose_name=_("Статус"),
        choices=Status.choices,
        default=Status.PUBLISHED,
        max_length=2,
        db_index=True,
    )
    photo = models.ImageField(
        verbose_name=_("Фото"), blank=True, upload_to="photos/posts/", null=True
    )
    saved = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("Сохраненные"),
        related_name="saved_posts",
        blank=True,
    )
    liked = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("Лайки"),
        related_name="liked_posts",
        blank=True,
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Автор"),
        on_delete=models.CASCADE,
        related_name="posts",
    )
    type = models.CharField(
        max_length=100,
        verbose_name=_("Тип контента"),
        default=Type.POST,
        choices=Type.choices,
    )
    tags = TaggableManager(blank=True, verbose_name=_("Теги"))
    published = PublishedManager()
    objects = models.Manager()  # The default manager

    class Meta:
        ordering = ["-time_create"]
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return [t.name for t in self.tags.all()]

    @property
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

    @property
    def url(self):
        return self.get_absolute_url()


class Comment(MPTTModel):
    like_field = "liked"

    class CommentManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name=_("Пост"), related_name="comments"
    )
    author = models.ForeignKey(
        get_user_model(), verbose_name=_("Автор"), on_delete=models.CASCADE
    )
    content = models.TextField()
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания")
    )
    time_update = models.DateTimeField(auto_now=True, verbose_name=_("Дата изменения"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))
    liked = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("Лайки"),
        related_name="liked_comments",
        blank=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="comment_parent",
        verbose_name=_("Родительский комментарий"),
    )
    objects = models.Manager
    active = CommentManager()

    class MPTTMeta:
        order_insertion_by = ["-time_create"]

    class Meta:
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create", "parent"])]
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")

    def __str__(self) -> str:
        return f"{self.author}: {self.content}"

    @property
    def get_avatar(self):
        if self.author:
            return self.author.profile.image
        return settings.DEFAULT_IMAGE_URL
