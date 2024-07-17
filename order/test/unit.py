from enum import StrEnum

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase, RequestFactory, TransactionTestCase

from order.models import Item
from order.repositories.carts import CartRepository
from order.repositories.items import ItemRepository
from order.repositories.orders import OrderRepository


class ItemGenres(StrEnum):
    ORDER_GENRES_IT = "IT"
    ORDER_GENRES_ELECTRONICS = "EL"
    ORDER_GENRES_TMP = "TM"


class TestItemCommand(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.item1 = ItemRepository.create(
            id=12,
            name="name1",
            description="descr1",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=12.1,
        )
        self.item2 = ItemRepository.create(
            id=13,
            name="name2",
            description="descr1",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=10.1,
        )
        self.item3 = ItemRepository.create(
            id=14,
            name="name3",
            description="descr3",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=2.1,
        )
        CartRepository.create(user=self.user)

    def test_add_item_in_cart_success(self):
        items: list[Item] = ItemRepository.filter(id__in=[12, 14, 13])
        self.assertEqual(len(items), 3)
        self.assertFalse([item for item in items if item.sold])
        user_cart = CartRepository.filter(user=self.user, is_snapshot=False).first()
        self.assertTrue(user_cart)
        CartRepository.add_items(user_cart, *items)
        self.assertTrue(len(CartRepository.get_items(user_cart)), 3)

    def test_add_item_in_cart_error(self):
        ItemRepository.delete(self.item3)
        items: list[Item] = ItemRepository.filter(id__in=[4, 5, 6])
        self.assertNotEqual(len(items), 3)


class TestOrderCommand(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.item1 = ItemRepository.create(
            name="name1",
            description="descr1",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=12.1,
        )
        self.item2 = ItemRepository.create(
            name="name2",
            description="descr1",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=10.1,
        )
        CartRepository.add_items(
            CartRepository.create(user=self.user), self.item1, self.item2
        )

    def test_make_order_success(self):
        user_cart = CartRepository.filter(user=self.user, is_snapshot=False).first()
        self.assertTrue(user_cart)
        user_cart_items: list[Item] = CartRepository.get_items(user_cart)
        self.assertTrue(user_cart_items)
        self.assertFalse([item for item in user_cart_items if item.sold is True])
        order = OrderRepository.create(cart_snapshot=user_cart, user=self.user)
        for item in user_cart_items:
            ItemRepository.update(item, sold=True)
        CartRepository.update(user_cart, is_snapshot=True)
        self.assertTrue(OrderRepository.get_bought_items(order))

    def test_make_order_error(self):
        user_cart = CartRepository.filter(user=self.user, is_snapshot=False).first()
        self.assertTrue(user_cart)
        user_cart_items: list[Item] = CartRepository.get_items(user_cart)
        self.assertTrue(user_cart_items)
        ItemRepository.update(self.item1, sold=True)
        self.assertTrue(
            [item for item in CartRepository.get_items(user_cart) if item.sold is True]
        )
