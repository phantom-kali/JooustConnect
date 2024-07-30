import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Group, GroupMessage, Notification
from django.contrib.auth import get_user_model
from dateutil import parser
from django.utils import timezone
from asgiref.sync import async_to_sync

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']
        timestamp = text_data_json.get('timestamp', timezone.now().isoformat())

        # Get sender's name
        sender_name = await self.get_user_name(sender_id)

        # Save message to database
        await self.save_message(sender_id, receiver_id, message, timestamp)

        # Create notification for receiver
        await self.create_dm_notification(sender_id, receiver_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'sender_name': sender_name,
                'receiver_id': receiver_id,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_name = event['sender_name']
        receiver_id = event['receiver_id']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_name': sender_name,
            'receiver_id': receiver_id,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def get_user_name(self, user_id):
        user = User.objects.get(id=user_id)
        return user.username

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message, timestamp):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=message,
            timestamp=parser.parse(timestamp)
        )

    @database_sync_to_async
    def create_dm_notification(self, sender_id, receiver_id, message):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        content = f"New message from {sender.username}: {message[:50]}..."  # Truncate long messages
        Notification.objects.create(
            user=receiver,
            content=content,
            timestamp=timezone.now()
        )
        
        # Send notification to receiver's notification group
        async_to_sync(self.channel_layer.group_send)(
            f'notifications_{receiver_id}',
            {
                'type': 'send_notification',
                'notification': {
                    'content': content,
                    'timestamp': timezone.now().isoformat()
                }
            }
        )

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs'].get('group_id')
        
        if not self.group_id:
            await self.close()
            return

        self.room_group_name = f'chat_group_{self.group_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        

    @database_sync_to_async
    def save_message(self, sender_id, group_id, content):
        sender = User.objects.get(id=sender_id)
        group = Group.objects.get(id=group_id)
        return GroupMessage.objects.create(sender=sender, group=group, content=content)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        group_id = text_data_json['group_id']
        timestamp = text_data_json.get('timestamp', timezone.now().isoformat())

        # Get sender's name
        sender_name = await self.get_user_name(sender_id)

        # Save group message to database
        await self.save_message(sender_id, group_id, message)

        # Create notifications for group members
        await self.create_group_notification(sender_id, group_id, message)

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'sender_name': sender_name,
                'group_id': group_id,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_name = event['sender_name']
        group_id = event['group_id']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_name': sender_name,
            'group_id': group_id,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def get_user_name(self, user_id):
        user = User.objects.get(id=user_id)
        return user.username
    
    @database_sync_to_async
    def create_group_notification(self, sender_id, group_id, message):
        sender = User.objects.get(id=sender_id)
        group = Group.objects.get(id=group_id)
        content = f"New message in {group.name} from {sender.username}: {message[:50]}..."  # Truncate long messages
        
        for member in group.members.exclude(id=sender_id):
            Notification.objects.create(
                user=member,
                content=content,
                timestamp=timezone.now()
            )
            
            # Send notification to each member's notification group
            async_to_sync(self.channel_layer.group_send)(
                f'notifications_{member.id}',
                {
                    'type': 'send_notification',
                    'notification': {
                        'content': content,
                        'timestamp': timezone.now().isoformat()
                    }
                }
            )

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.notification_group_name = f'notifications_{self.user.id}'

        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        notification = event['notification']

        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))