from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.auth import get_user, logout
from django.contrib.auth.models import User

class WatchConsumer(WebsocketConsumer):

    # Connect to socket and join room/group
    def websocket_connect(self, event):
        self.room_name = self.scope['url_route']['kwargs']['video_id']
        self.room_group_name = 'watch_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        user = self.scope['user']
        if user.is_authenticated:
          async_to_sync(self.channel_layer.group_add)(
              user.username,
              self.channel_name
          )

        self.accept()
        print (self.room_name)
        print (self.room_group_name)

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']

        self.send(text_data=json.dumps({
            'content': content,
        }))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'comment',
                'content': content,
            }
        )

    def comment(self, event):
        content = event['content']

        self.send(text_data=json.dumps({
            'content': content,
        }))
