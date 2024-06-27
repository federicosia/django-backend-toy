from django.contrib.auth.models import User
from django.core.exceptions import BadRequest

from order.models import Item, Order
from order.repositories.items import ItemRepository
from order.repositories.orders import OrderRepository


def create_order_from_item_ids(ids: list[int], user: User):
    items: list[Item] = ItemRepository.filter(id__in=ids)
    if len(items) == len(ids):
        order_price: float = 0
        for item in items:
            order_price += item.price
        OrderRepository.create(price=order_price, items=len(items), user=user)
        return True
    else:
        raise BadRequest
