import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        user = self.scope['user']

        if not user.is_authenticated:
            await self.close()
            return

        has_access = await self.check_access(user, self.room_id)
        if not has_access:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        content = data.get('message', '').strip()
        if not content:
            return

        user = self.scope['user']
        message = await self.save_message(user, self.room_id, content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content,
                'username': user.username,
                'user_id': user.id,
                'timestamp': message.created_at.strftime('%H:%M'),
                'avatar': user.avatar.url if user.avatar else None,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def check_access(self, user, room_id):
        from .models import ChatRoom
        try:
            room = ChatRoom.objects.get(pk=room_id)
            return room.participants.filter(pk=user.pk).exists()
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, room_id, content):
        from .models import ChatRoom, Message
        room = ChatRoom.objects.get(pk=room_id)
        return Message.objects.create(room=room, sender=user, content=content)
