from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликовано'
    name = models.CharField(verbose_name = 'Название', max_length=100, db_index = True)
    content = models.TextField(verbose_name = 'Контент')
    time_create = models.DateTimeField(verbose_name = 'Дата создания', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name = 'Дата обновления', auto_now=True)
    time_publish = models.DateTimeField(verbose_name = 'Дата публикации', default = timezone.now)
    status = models.CharField(verbose_name = 'Статус', choices = Status.choices, default = Status.PUBLISHED, max_length = 2)
    photo = models.ImageField(blank=True, upload_to = 'photos/posts/', null=True)
    count_views = models.IntegerField(default=0)
    liked = models.ManyToManyField(get_user_model(), verbose_name = 'Лайки', related_name='post_like', blank = True, related_query_name='post_likes')
    comment = models.ManyToManyField("Comment", blank = True, related_name = 'post_comment', related_query_name='comment')
    author = models.ForeignKey(get_user_model(), verbose_name="Автор", on_delete=models.CASCADE, related_name = 'post_author')
    tags = TaggableManager(blank=True)
    published = PublishedManager()
    objects = models.Manager() # The default manager


    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.name
    
    @property
    def num_likes(self):
        return self.liked.count()
    
    @property
    def num_comments(self):
        return self.comment.count()
    
    @property
    def up_post_views(self):
        self.post_views += 1
        self.save()
    

    def get_absolute_url(self):
        return reverse("posts:detail-post", kwargs={"post_id": self.pk})
    
# LIKES_CHOICES = (
#     ("Like", "Like"),
#     ("Unlike", "Unlike")
# )  
    
# class Like(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
#     post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)

    
    # class Meta:
    #     unique_together = ('user', 'post')
    
    # def __str__(self) -> str:
    #     return str(self.post)
    
class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_active = models.BooleanField(default = True)
    likes = models.ManyToManyField(get_user_model(), verbose_name = 'Лайки', related_name='comment_like', blank = True, related_query_name='comment_likes')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank = True, null=True, related_name = "replies")
    
    
    def __str__(self) -> str:
        return f'{self.author}: {self.text}'
    

    
    
    
