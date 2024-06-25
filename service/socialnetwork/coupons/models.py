from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


# Create your models here.
class Coupon(models.Model):
    """ Model for storing coupon data. """
    class CouponManager(models.Manager):
        """Manager for managing active coupons."""
        def get_queryset(self):
            return (
                super()
                .get_queryset()
                .filter(valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            )

    code = models.CharField(
        verbose_name=_("Coupon code"),
        max_length=50,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]*$",
                message="Only alphanumeric characters are allowed.",
            )
        ],
    )
    valid_from = models.DateTimeField(verbose_name=_("Valid from"))
    valid_to = models.DateTimeField(verbose_name=_("Valid to"))
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Discount in %"),
    )
    active_objects = CouponManager()
    objects = models.Manager()

    def __str__(self) -> str:
        return self.code

    @property
    def is_expired(self) -> bool:
        """Check whether coupon is_expired."""
        return self.valid_to < timezone.now()
