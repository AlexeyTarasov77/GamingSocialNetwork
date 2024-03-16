from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart-view'),
    path('add/', views.cart_add_or_update, name='cart-add-or-update'),
    path('remove/', views.cart_remove, name='cart-remove'),
]
