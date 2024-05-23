from channels.generic.websocket import AsyncWebsocketConsumer
from gameblog.redis_connection import r

class UserStatusConsumer(AsyncWebsocketConsumer):        
    async def update_user_status(self, user_id, status: int): # 1 - online, 0 - offline
        client = r
        client.incr(f"user:{user_id}:status")  if status else client.decr(f"user:{user_id}:status")
        # client.aclose()    
    
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
 
