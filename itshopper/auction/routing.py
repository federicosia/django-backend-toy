# auction/routing.py
from django.urls import re_path

from auction.consumers import AuctionConsumer

websocket_urlpatterns = [
    re_path(r"auction", AuctionConsumer.as_asgi()),
]
