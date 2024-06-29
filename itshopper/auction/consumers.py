# auction/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class AuctionConsumer(WebsocketConsumer):
    def connect(self):
        # join the auction group
        async_to_sync(self.channel_layer.group_add)("auction", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # leave the auction group
        async_to_sync(self.channel_layer.group_discard)("auction", self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            "auction", {"type": "auction.message", "message": message}
        )

    # Receive message from room group
    def auction_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
