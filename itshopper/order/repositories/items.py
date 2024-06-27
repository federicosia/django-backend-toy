from .base import BaseRepository
from order.models import Item


class ItemRepository(BaseRepository):
    model = Item
