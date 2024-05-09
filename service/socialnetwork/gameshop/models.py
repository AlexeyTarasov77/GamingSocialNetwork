from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.conf import settings
import os

from gameblog.mixins import SaveSlugMixin


# Create your models here.
class Product(SaveSlugMixin, models.Model):
    """
    A model representing a product.
    """

    AVAILABLE_CHOICES = (
        (True, "В наличии"),
        (False, "Нет в наличии"),
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )
    title = models.CharField("Название", max_length=250)
    brand = models.CharField("Бренд", max_length=250)
    description = models.TextField("Описание", blank=True, null=True)
    slug = models.SlugField("URL", max_length=250, blank=True)
    price = models.DecimalField("Цена", max_digits=7, decimal_places=2, default=0)
    image = models.ImageField(
        "Изображение",
        upload_to="photos/gameshop/products",
        default="photos/default.jpeg",
    )
    available = models.BooleanField(
        "Наличие", default=AVAILABLE_CHOICES[0][0], choices=AVAILABLE_CHOICES
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)
    discount = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        super().save(*args, slug_field="slug", slugify_field="title", **kwargs)

    def get_absolute_url(self):
        return reverse("shop:products-detail", kwargs={"slug": self.slug})

    @property
    def url(self):
        return self.get_absolute_url()
    
    def __str__(self):
        return self.title

    @property
    def final_price(self):
        price = self.price - (self.price * self.discount / 100) # вычисление суммы с возможной скидкой 
        return round(price, 2)
    
    def get_category(self):
        return self.category if self.category else 'Без категории'
    
    def get_image(self):
        if not self.image:
            return os.path.join(settings.MEDIA_ROOT, 'photos/default.jpeg')
        return self.image.url
    
    def _category(self):
        return self.get_category()
    
    def _available(self):
        return self.get_available_display()



class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True


class Category(SaveSlugMixin, models.Model):
    name = models.CharField("Категория", max_length=250, db_index=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", blank=True, null=True
    )
    slug = models.SlugField(
        "URL", max_length=250, unique=True, null=False, editable=True, blank=True
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        unique_together = ("slug", "parent")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        super().save(*args, slug_field="slug", slugify_field="name", **kwargs)

    def __str__(self) -> str:
        full_path = [self.name]
        k = self.parent
        while k is not None:  # пока у категории есть родитель формируем путь
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(
            full_path[::-1]
        )  # возвращаем конечную иерархию категорий в обратном порядке

    def get_absolute_url(self):
        return reverse("shop:category-list", args=[self.slug])
