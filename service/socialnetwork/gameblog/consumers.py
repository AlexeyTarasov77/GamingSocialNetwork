from channels.generic.websocket import AsyncWebsocketConsumer
from core.redis_connection import r


class UserStatusConsumer(AsyncWebsocketConsumer):
    """Consumer to track users status (online/offline)."""

    async def update_user_status(self, user_id, status: int):  # 1 - online, 0 - offline
        """Updating status for current user in redis"""
        client = r
        (
            client.incr(f"user:{user_id}:status")
            if status
            else client.decr(f"user:{user_id}:status")
        )
        # client.aclose()

    async def connect(self):
        """Increase status on ws connect"""
        await self.accept()
        # await self.channel_layer.group_add("users", self.channel_name)

        user = self.scope["user"]
        if user.is_authenticated:
            await self.update_user_status(user.id, 1)

    async def disconnect(self, code):
        """Decrease status on ws disconnect"""
        # await self.channel_layer.group_discard("users", self.channel_name)

        user = self.scope["user"]
        if user.is_authenticated:
            await self.update_user_status(user.id, 0)
