from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import ProductProxy, Category

# Create your views here.
class ProductListView(generic.ListView):
    template_name = "gameshop/products_list.html"
    context_object_name = "products"
    paginate_by = 15

    def get_queryset(self):
        cat = self.kwargs.get("cat_slug")
        queryset = ProductProxy.objects.select_related("category")
        if cat:
            queryset = queryset.filter(category__slug=cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get("cat_slug")
        if cat_slug:
            category = get_object_or_404(Category, slug=cat_slug)
        context["category"] = category.name if cat_slug else 'Все категории'
        return context
    
class ProductDetailView(generic.DetailView):
    queryset = ProductProxy.objects.select_related("category")
    template_name = "gameshop/products_detail.html"
    context_object_name = "product"
    

# def category_list(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     products = ProductProxy.objects.select_related("category").filter(category=category)
#     context = {"products": products, "category": category}
#     return render(request, "gameshop/category_list.html", context)
