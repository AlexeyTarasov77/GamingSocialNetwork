from collections.abc import Iterable
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200, db_index = True)
    content = models.TextField()
    photo = models.ImageField(blank=True, upload_to='photos/articles')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'article_author')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", editable = False)
    time_create = models.DateTimeField(verbose_name = 'Дата создания', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name = 'Дата обновления', auto_now=True)
    tags = TaggableManager(blank=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        counter = 0
        while Article.objects.filter(slug = self.slug).exists():
            counter += 1
            self.slug += counter
        return super.save(*args, **kwargs)

    class Meta:
        ordering = ['-time_create']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"slug": self.slug})

