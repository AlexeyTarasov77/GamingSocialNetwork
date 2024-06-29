from decimal import Decimal
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from gameblog.mixins import SaveSlugMixin


class Product(SaveSlugMixin, models.Model):
    """
    A product model that includes fields for category, title, brand, description,
    slug, price, image, available, created_at, updated_at, and discount.
    """

    AVAILABLE_CHOICES = (
        (True, "В наличии"),
        (False, "Нет в наличии"),
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
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
        """
        Overrides the save method of the parent class to save the slug field.
        """
        super().save(*args, slug_field="slug", slugify_value=self.title, **kwargs)

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for this product.

        Returns:
            str: The absolute URL for this product.
        """
        return reverse("shop:products-detail", kwargs={"slug": self.slug})

    @property
    def url(self) -> str:
        """
        Returns the URL for this product.

        Returns:
            str: The URL for this product.
        """
        return self.get_absolute_url()

    def __str__(self) -> str:
        """
        Returns a string representation of this product.

        Returns:
            str: The string representation of this product.
        """
        return self.title

    @property
    def final_price(self) -> Decimal:
        """
        Calculates the final price with potential discount.

        Returns:
            float: The final price with potential discount.
        """
        price = self.price - (self.price * self.discount / 100)
        return round(price, 2)

    def get_category(self) -> str:
        """
        Returns the category of this product or 'Без категории' if no category is set.

        Returns:
            str: The category of this product or 'Без категории' if no category is set.
        """
        return self.category if self.category else 'Без категории'

    def get_image(self) -> str:
        """
        Returns the URL for the image of this product or the default image URL if no image is set.

        Returns:
            str: The URL for the image of this product or the default image URL if no image is set.
        """
        if not self.image:
            return settings.DEFAULT_IMAGE_URL
        return self.image.url

    def _category(self) -> str:
        """
        Returns the category of this product.

        Returns:
            str: The category of this product.
        """
        return self.get_category()

    def _available(self) -> str:
        """
        Returns the display value for the available field.

        Returns:
            str: The display value for the available field.
        """
        return self.get_available_display()


class ProductManager(models.Manager):
    """Queryset manager for the Product model."""
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    """Proxy model for Product which uses the ProductManager."""
    objects = ProductManager()

    class Meta:
        proxy = True


class Category(SaveSlugMixin, models.Model):
    """
    A model representing a category of products.
    """
    name = models.CharField(
        max_length=250,
        db_index=True,
        verbose_name="Категория",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        verbose_name="Родительская категория",
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        null=False,
        editable=True,
        blank=True,
        verbose_name="URL",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        unique_together = ("slug", "parent")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        """
        Overrides the save method of the parent class to save the slug field.
        """
        super().save(*args, slug_field="slug", slugify_value="name", **kwargs)

    def __str__(self) -> str:
        """
        Returns the string representation of this category.

        Returns:
            str: The string representation of this category.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:  # пока у категории есть родитель формируем путь
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(
            full_path[::-1]
        )  # возвращаем конечную иерархию категорий в обратном порядке

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for this category.

        Returns:
            str: The absolute URL for this category.
        """
        return reverse("shop:category-list", args=[self.slug])
