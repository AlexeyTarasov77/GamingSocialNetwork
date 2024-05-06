from algoliasearch_django import AlgoliaIndex, register
from algoliasearch_django.decorators import register
from .models import Post

@register(Post)
class PostsIndex(AlgoliaIndex):
    should_index = 'is_published'
    fields = ['title', 'content', 'author', 'get_status_display', 'url', 'get_type_display']
    index_name = 'posts'
    tags = 'tag_list'
    settings = {
        'searchableAttributes': ['title', 'content'],
        'attributesForFaceting': ['author', 'get_status_display', 'get_type_display']
    }

