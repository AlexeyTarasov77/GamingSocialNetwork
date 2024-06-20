from django.contrib import admin
from .models import Message, ChatRoom

# Register your models here.
admin.site.register(Message)    

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'id', 'is_group')
    search_fields = ('name', 'id')