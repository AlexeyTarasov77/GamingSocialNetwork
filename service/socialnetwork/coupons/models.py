from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
# Create your models here.
class Coupon(models.Model):
    class CouponManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        validators=
            [RegexValidator(regex=r'^[a-zA-Z0-9]*$', message="Only alphanumeric characters are allowed.")])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active_objects = CouponManager()
    objects = models.Manager()
    
    def __str__(self) -> str:
        return self.code 
    
    @property
    def is_active(self):
        return self.valid_from <= timezone.now() <= self.valid_to