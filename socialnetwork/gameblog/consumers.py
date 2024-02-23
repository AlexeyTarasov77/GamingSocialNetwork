import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import Profile
from django.db.models import F

class UserStatusConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def update_user_incr(self, user):
        Profile.objects.filter(user=user).update(online=F('online') + 1)

    @database_sync_to_async
    def update_user_decr(self, user):
        Profile.objects.filter(user=user).update(online=F('online') - 1)
    
    # async def connect(self):
    #     user = self.scope["user"]
    #     await self.update_user_incr(user)
    #     # await self.accept()
        
    # async def receive(self, text_data=None, bytes_data=None):
    #     pass
        
    # async def disconnect(self, code):
    #     user = self.scope["user"]
    #     await self.update_user_decr(user)
        
    async def connect (self):
        await self.accept ()
        await self.channel_layer.group_add ("users", self.channel_name)
 
        user = self.scope ['user']
        if user.is_authenticated:
            await self.update_user_incr(user)
    
    async def disconnect (self, code):
        await self.channel_layer.group_discard ("users", self.channel_name)
 
        user = self.scope ['user']
        if user.is_authenticated:
            await self.update_user_decr(user)
 
