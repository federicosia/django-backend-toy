from .base import BaseRepository
from order.models import Cart


class CartRepository(BaseRepository):
    model = Cart

    @classmethod
    def add_items(cls, user_cart: Cart, *items):
        try:
            for item in items:
                user_cart.items.add(item)
        except TypeError:
            return None

    @classmethod
    def get_items(cls, user_cart: Cart):
        return user_cart.items.all()
