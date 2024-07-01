from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create_view, name="order_create"),
    path("detail/<int:order_id>/", views.order_detail_view, name="order_detail"),
    path("order/<int:order_id>/pdf/", views.order_to_pdf, name="order_pdf"),
]
