from . import views
from django.urls import path

app_name = 'orders'

urlpatterns = [
    path("create/", views.order_create_view, name="order_create"),
    path("detail/<int:order_id>/", views.order_detail_view, name="order_detail")
]
