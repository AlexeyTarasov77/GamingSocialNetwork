from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from .mixins import SaveSlugMixin


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
        "Category", on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField("Название", max_length=250)
    brand = models.CharField("Бренд", max_length=250)
    description = models.TextField("Описание", blank=True)
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

    def __str__(self):
        return self.title

    @property
    def get_price(self):
        if self.price == 0:
            return mark_safe("<span class='text-success'>Бесплатно</span>")
        return f"$ {self.price}"
    
    @property
    def get_category(self):
        return self.category if self.category else 'Без категории'

    @property
    def get_discounted_price(self):
        discounted_price = self.price - (self.price * self.discount / 100)
        return round(discounted_price, 2)


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
        return reverse("shop:category-list", kwargs={"slug": self.slug})
