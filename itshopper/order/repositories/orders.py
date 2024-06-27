from .base import BaseRepository
from order.models import Order


class OrderRepository(BaseRepository):
    model = Order
