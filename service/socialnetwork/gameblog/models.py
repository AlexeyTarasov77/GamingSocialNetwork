from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Ad(models.Model):
    """
    Model for representing important ads posted on the main page.

    Attributes:
        title (str): The title of the ad.
        description (str): The description of the ad. Optional.
        attached_file (File): The attached file of the ad. Optional.
        time_create (datetime): The time when the ad was created.
    """
    title = models.CharField(
        max_length=50,
        verbose_name=_("title")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("description")
    )
    attached_file = models.FileField(
        upload_to="files/gameblog",
        blank=True,
        null=True,
        verbose_name=_("attached file")
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("time create")
    )

    def __str__(self) -> str:
        return self.title


class BackgroundVideo(models.Model):
    """
    Model for representing a background video which appears on the main page.

    Attributes:
        video_url (str): The URL of the video.
    """
    video_url = models.URLField(max_length=255, verbose_name=_("video url"))

    def __str__(self) -> str:
        return self.video_url
