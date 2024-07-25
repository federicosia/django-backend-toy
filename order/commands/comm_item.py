from dataclasses import dataclass

from django.contrib.auth.models import User
from django.core.exceptions import BadRequest

from order.commands.command import Command
from order.models import Item, Cart
from order.repositories.carts import CartRepository
from order.repositories.items import ItemRepository


@dataclass
class AddItemInCart(Command):
    ids: list[int]
    user: User

    def handle(self):
        items: list[Item] = ItemRepository.filter(id__in=self.ids)
        if len(items) == len(self.ids):
            user_cart: Cart = CartRepository.filter(
                user=self.user, is_snapshot=False
            ).first()
            if user_cart:
                CartRepository.add_items(user_cart, *items)
            else:
                user_cart: Cart = CartRepository.create(user=self.user)
                CartRepository.add_items(user_cart, *items)
            return user_cart
        else:
            raise BadRequest


@dataclass
class SearchItem(Command):
    search_string: str

    def handle(self):
        return list(
            ItemRepository.contains_field_substring(self.search_string).values()
        )
