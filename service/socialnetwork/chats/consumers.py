from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import ChatRoom, Message
import json
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope['user']
        self.chatroom = await sync_to_async(get_object_or_404)(ChatRoom, id=self.chat_id)

        await self.accept()

    async def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        msg_body = data_json.get('body')
        
        message = await sync_to_async(Message.objects.create)(
            chat=self.chatroom,
            author=self.user,
            body=msg_body
        )
        html = render_to_string(
            'chats/includes/chat_message_p.html',
            {
                'message': message,
                'user': self.user
            }
        )
        await self.send(text_data=html)