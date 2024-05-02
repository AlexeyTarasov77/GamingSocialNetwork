from algoliasearch_django import AlgoliaIndex, register
from algoliasearch_django.decorators import register
from .models import Post

@register(Post)
class PostsIndex(AlgoliaIndex):
    should_index = 'is_published'
    fields = ['name', 'content', 'author', 'status']
    index_name = 'posts'
    tags = 'tags'
