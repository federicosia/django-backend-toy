from .base import BaseRepository
from order.models import Order


class OrderRepository(BaseRepository):
    model = Order

    @classmethod
    def get_bought_items(cls, order: Order):
        return order.cart_snapshot.items.all()
