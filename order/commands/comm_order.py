from dataclasses import dataclass
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.db import transaction

from order.commands.command import Command

from order.models import Cart, Item, Order
from order.repositories.carts import CartRepository
from order.repositories.items import ItemRepository
from order.repositories.orders import OrderRepository


@dataclass
class MakeOrder(Command):
    user: User

    def handle(self) -> Order:
        user_cart: Cart = CartRepository.filter(
            user=self.user, is_snapshot=False
        ).first()
        if user_cart:
            user_cart_items: list[Item] = CartRepository.get_items(user_cart)
            if (
                user_cart
                and len(user_cart_items) > 0
                and len([item for item in user_cart_items if item.sold is True]) == 0
            ):
                with transaction.atomic():
                    OrderRepository.create(cart_snapshot=user_cart, user=self.user)
                    for item in user_cart_items:
                        ItemRepository.update(item, sold=True)
                    order: Order = CartRepository.update(user_cart, is_snapshot=True)
                return order
        raise BadRequest
