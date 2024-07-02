from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.db import transaction

from order.models import Item, Cart
from order.repositories.items import ItemRepository
from order.repositories.orders import OrderRepository
from order.repositories.carts import CartRepository
from setup_logs import setup_logging

log_setup = setup_logging()
logger_console = log_setup.getLogger("console")


class OrderLogic:
    @staticmethod
    def create_order_from_cart(
        user: User,
    ):
        user_cart: Cart = CartRepository.filter(user=user, is_snapshot=False).first()
        user_cart_items: list[Item] = CartRepository.get_items(user_cart)
        if (
            user_cart
            and len(user_cart_items) > 0
            and len([item for item in user_cart_items if item.sold is True]) == 0
        ):
            with transaction.atomic():
                OrderRepository.create(cart_snapshot=user_cart, user=user)
                for item in user_cart_items:
                    ItemRepository.update(item, sold=True)
                CartRepository.update(user_cart, is_snapshot=True)
            return True
        else:
            logger_console.error(
                f"items in cart -> {len(user_cart_items)} and "
                f"items already sold -> {len([item for item in user_cart_items if item.sold is True])}"
            )
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
                CartRepository.add_items(user_cart, items)
            else:
                user_cart: Cart = CartRepository.create(user=user)
                CartRepository.add_items(user_cart, items)
            return True
        else:
            raise BadRequest

    @staticmethod
    def search_for_items(item_string: str):
        return list(ItemRepository.contains_field_substring(item_string).values())
