from django.db import models

# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    attached_file = models.FileField(upload_to='files/gameblog', blank=True)
    time_create = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.title
    
class BackgroundVideo(models.Model):
    video_url = models.URLField(max_length=255)
    def __str__(self) -> str:
        return self.video_url

