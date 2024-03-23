from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/<int:product_id>/', views.cart_add_or_update, name='add'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove'),
]
