from algoliasearch_django import AlgoliaIndex, register
from algoliasearch_django.decorators import register
from .models import Post

@register(Post)
class PostsIndex(AlgoliaIndex):
    should_index = 'is_published'
    fields = ['title', 'content', 'author', 'status', 'url']
    index_name = 'posts'
    tags = 'tag_list'
    settings = {
        'searchableAttributes': ['title', 'content'],
        'attributesForFaceting': ['author', 'status']
    }
