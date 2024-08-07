from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products-list"),
    path(
        "category/<slug:cat_slug>/",
        views.ProductListView.as_view(),
        name="category-list",
    ),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="products-detail"),
]
