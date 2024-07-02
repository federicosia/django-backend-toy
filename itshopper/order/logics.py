from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.db import transaction

from order.models import Item, Cart
from order.repositories.items import ItemRepository
from order.repositories.orders import OrderRepository
from order.repositories.carts import CartRepository


class OrderLogic:
    @staticmethod
    def create_order_from_cart(user: User):
        user_cart: Cart = CartRepository.filter(user=user, is_snapshot=False).first()
        user_cart_items: list[Item] = ItemRepository.filter(cart=user_cart)
        if user_cart and len(user_cart_items) > 0:
            with transaction.atomic():
                OrderRepository.create(cart_snapshot=user_cart, user=user)
                for item in user_cart_items:
                    ItemRepository.update(item, sold=True)
                CartRepository.update(user_cart, is_snapshot=True)
            return True
        else:
            raise BadRequest


class ItemLogic:
    @staticmethod
    def add_item_in_cart(item_ids: list[int], user: User):
        items: list[Item] = ItemRepository.filter(id__in=item_ids)
        if len(items) == len(item_ids):
            user_cart: Cart = CartRepository.filter(
                user=user, is_snapshot=False
            ).first()
            if user_cart:
                for item in items:
                    ItemRepository.update(item, cart=user_cart)
            else:
                user_cart: Cart = CartRepository.create(user=user)
                for item in items:
                    ItemRepository.update(item, cart=user_cart)
            return True
        else:
            raise BadRequest

    @staticmethod
    def search_for_items(item_string: str):
        return list(ItemRepository.contains_field_substring(item_string).values())
