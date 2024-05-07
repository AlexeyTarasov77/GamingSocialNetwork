from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product


@register(Product)
class ProductIndex(AlgoliaIndex):
    fields = [
        "title",
        "description",
        "final_price",
        "category",
        "brand",
        "url",
        "_category",
        "_available",
    ]
    settings = {
        "searchableAttributes": ["title", "description", "brand"],
        "attributesForFaceting": ["_category", "_available"],
    }
    index_name = "products"
