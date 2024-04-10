from django.db import models
from django.urls import reverse
from gameshop.models import Product
from django.contrib.auth import get_user_model
# Create your models here.

class Order(models.Model):
    PAID_STATUS_CHOICES = (
        (True, 'Оплачено'),
        (False, 'В ожидании'),
    )
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250) 
    postal_code = models.CharField(max_length=20) 
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    paid = models.BooleanField(default=False, choices=PAID_STATUS_CHOICES) # оплачен заказ или же нет
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, related_name="orders")
    class Meta:
        ordering = ['-created']
        indexes = [ models.Index(fields=['-created']),
        ]
    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_absolute_url(self):
        return reverse("orders:order_detail",args=[self.pk])
    
class OrderItem(models.Model):
    order = models.ForeignKey("Order",
        related_name='items',
        on_delete=models.CASCADE) 
    product = models.ForeignKey(Product,
        related_name='order_items',
        on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self): 
        return self.product.title
    def get_cost(self):
        return self.price * self.quantity