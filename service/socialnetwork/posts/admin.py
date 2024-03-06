from django.contrib import admin
from .models import Post, Comment
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'post', 'author', 'content', 'time_create', 'is_active']
    list_display_links = ['post']
    list_editable = ['is_active']