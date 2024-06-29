from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from django.utils.translation import gettext as _
from django.conf import settings


class PublishedManager(models.Manager):
    """
    A manager that returns only published posts.

    This manager filters the queryset to only include posts with a status of
    "PUBLISHED".
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    """
    Represents a post in the social network.
    """

    like_field = "liked"

    class Status(models.TextChoices):
        """
        Represents the status of the post.
        """
        DRAFT = "DF", _("Draft")
        PUBLISHED = "PB", _("Published")

    class Type(models.TextChoices):
        """
        Represents the type of the post.
        """
        NEWS = "NW", _("News")
        ARTICLE = "AR", _("Article")
        POST = "PS", _("Post")

    title: str = models.CharField(
        verbose_name=_("Post title"), max_length=100, db_index=True
    )
    content: str = models.TextField(verbose_name=_("Post content"))
    time_create = models.DateTimeField(
        verbose_name=_("Post creation date"), auto_now_add=True
    )
    time_update = models.DateTimeField(
        verbose_name=_("Post update date"), auto_now=True
    )
    time_publish = models.DateTimeField(
        verbose_name=_("Post publication date"), default=timezone.now
    )
    status: Status = models.CharField(
        verbose_name=_("Post status"),
        choices=Status.choices,
        default=Status.PUBLISHED,
        max_length=2,
        db_index=True,
    )
    photo = models.ImageField(
        verbose_name=_("Post photo"),
        blank=True,
        upload_to="photos/posts/",
        null=True,
    )
    saved = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("Saved posts"),
        related_name="saved_posts",
        blank=True,
    )
    liked = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("Post likes"),
        related_name="liked_posts",
        blank=True,
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Post author"),
        on_delete=models.CASCADE,
        related_name="posts",
    )
    type: Type = models.CharField(
        max_length=100,
        verbose_name=_("Post type"),
        default=Type.POST,
        choices=Type.choices,
    )
    tags: TaggableManager = TaggableManager(
        blank=True, verbose_name=_("Post tags")
    )
    published = PublishedManager()
    objects = models.Manager()

    class Meta:
        ordering = ["-time_create"]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self) -> str:
        """
        Return the string representation of the post.
        """
        return self.title

    @property
    def tag_list(self) -> list[str]:
        """
        Return the list of tags associated with the post.
        """
        return [t.name for t in self.tags.all()]

    @property
    def is_published(self) -> bool:
        """
        Return whether the post is published.
        """
        return self.status == Post.Status.PUBLISHED

    @property
    def num_likes(self) -> int:
        """
        Return the number of likes the post has.
        """
        return self.liked.count()

    @property
    def num_comments(self) -> int:
        """
        Return the number of comments the post has.
        """
        return self.comments.count()

    def get_absolute_url(self) -> str:
        """
        Return the absolute URL of the post.
        """
        return reverse("posts:detail-post", kwargs={"post_id": self.pk})

    @property
    def url(self) -> str:
        """
        Return the URL of the post.
        """
        return self.get_absolute_url()


class Comment(MPTTModel):
    """
    Represents a comment on a post.
    """

    like_field = "liked"

    class CommentManager(models.Manager):
        """
        Manager for active comments.
        """

        def get_queryset(self):
            """
            Return only active comments.
            """
            return super().get_queryset().filter(is_active=True)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name=_("Post"), related_name="comments"
    )
    author = models.ForeignKey(
        get_user_model(), verbose_name=_("Author"), on_delete=models.CASCADE
    )
    content = models.TextField()
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )
    time_update = models.DateTimeField(auto_now=True, verbose_name=_("Update date"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    liked = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("Likes"),
        related_name="liked_comments",
        blank=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="comment_parent",
        verbose_name=_("Parent comment"),
    )
    objects = models.Manager
    active = CommentManager()

    class MPTTMeta:
        order_insertion_by = ["-time_create"]

    class Meta:
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create", "parent"])]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self) -> str:
        """
        Return a string representation of the comment.
        """
        return f"{self.author}: {self.content}"

    @property
    def get_avatar(self) -> str:
        """
        Return the avatar of the author.
        """
        if self.author:
            return self.author.profile.image
        return settings.DEFAULT_IMAGE_URL
