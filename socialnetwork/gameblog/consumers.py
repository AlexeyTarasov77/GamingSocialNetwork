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
    
    async def connect(self):
        user = self.scope["user"]
        await self.update_user_incr(user)
        await self.accept()
        
    async def disconnect(self, code):
        user = self.scope["user"]
        await self.update_user_decr(user)
        await super().disconnect(code)
        