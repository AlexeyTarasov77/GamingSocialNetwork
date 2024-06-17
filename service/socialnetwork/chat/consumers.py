from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message
import json
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'chat_%s' % self.chat_id

        # Join chat 
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    async def receive_json(self, content):
        match content.get('type'):
            case 'disconnect':
                self.channel_layer.group_send(
                    content['id'],
                    {
                        'type': 'disconnect',
                        'id': content['id']
                    }
                )
            case 'invite':
                self.channel_layer.group_send(
                    content['id'],
                    {
                        'type': 'invite',
                        'id': content['id']
                    }
                )
                
        

    # Receive message from room group
    async def chat_message(self, event):
        match event.get('type'):
            case 'disconnect':
                await self.channel_layer.group_discard(
                    event['id'],
                    self.channel_name
                )
            case 'invite':
                sync_to_async(Chat.objects.get)(id=event['id']).users.add(self.scope['user'])
                await self.group_add(event['id'], self.channel_name)