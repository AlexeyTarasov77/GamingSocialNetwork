from channels.generic.websocket import AsyncWebsocketConsumer
from users.models import Profile
from django.db.models import F
import redis.asyncio as redis
from django.conf import settings

redis_settings = {"host": settings.REDIS_HOST, "port": settings.REDIS_PORT, "db": settings.REDIS_DB, "decode_responses": True}
r = redis.Redis

class UserStatusConsumer(AsyncWebsocketConsumer):        
    async def update_user_status(self, user_id, status: int): # 1 - online, 0 - offline
        client = await r(**redis_settings)
        await client.incr(f"user:{user_id}:status")  if status else await client.decr(f"user:{user_id}:status")
        client.aclose()    
    
    async def connect (self):
        await self.accept ()
        # await self.channel_layer.group_add("users", self.channel_name)
 
        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user.id, 1)
    
    async def disconnect (self, code):
        # await self.channel_layer.group_discard("users", self.channel_name)
 
        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user.id, 0)
 
