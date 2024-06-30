from .base import BaseRepository
from order.models import Cart


class CartRepository(BaseRepository):
    model = Cart
