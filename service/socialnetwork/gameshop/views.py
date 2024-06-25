from typing import Any
from .recommender import Recommender
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import ProductProxy, Category


# Create your views here.
class ProductListView(generic.ListView):
    """View for listing all products"""
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
        """Add current category to context"""
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get("cat_slug")
        if cat_slug:
            category = get_object_or_404(Category, slug=cat_slug)
        context["category"] = category.name if cat_slug else "Все категории"
        return context


class ProductDetailView(generic.DetailView):
    """View for product detail page"""
    queryset = ProductProxy.objects.select_related("category")
    template_name = "gameshop/products_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add suggested products to context"""
        context = super().get_context_data(**kwargs)
        rec = Recommender()
        context["recommended_products"] = rec.suggest_products_for([self.object])
        return context
