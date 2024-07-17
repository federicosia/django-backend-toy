from enum import StrEnum

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from order.models import Cart, Item
from order.repositories.carts import CartRepository
from order.views import create_order, add_item_in_cart, search_item
from order.schemas.item_schema import AddItemInput
from order.repositories.items import ItemRepository


class ItemGenres(StrEnum):
    ORDER_GENRES_IT = "IT"
    ORDER_GENRES_ELECTRONICS = "EL"
    ORDER_GENRES_TMP = "TM"


# Create your tests here.
class OrderTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.cart_order_success: Cart = CartRepository.create(user=self.user)

        # create fake items
        self.item1: Item = ItemRepository.create(
            name="item1",
            description="descr1",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=12.2,
        )
        self.item2: Item = ItemRepository.create(
            name="item2",
            description="descr2",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=9.2,
        )
        self.item3: Item = ItemRepository.create(
            name="item3",
            description="descr3",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=7.2,
        )

    def test_create_order_made_successfully(self):
        self.client.login(username="testuser", password="testpassword")
        request_order = self.factory.post("/order/create")
        setattr(request_order, "user", self.user)
        CartRepository.add_items(
            self.cart_order_success, self.item1, self.item2, self.item3
        )
        create_order_status_code: tuple = create_order(request_order)[0]
        self.assertEqual(create_order_status_code, 202)
        self.assertTrue(CartRepository.get(pk=self.cart_order_success.pk).is_snapshot)
        for item in CartRepository.get_items(self.cart_order_success):
            self.assertTrue(item.sold)

    def test_create_order_made_unsuccessfully(self):
        self.client.login(username="testuser", password="testpassword")
        request_order = self.factory.post("/order/create")
        setattr(request_order, "user", self.user)
        CartRepository.add_items(
            self.cart_order_success, self.item1, self.item2, self.item3
        )
        ItemRepository.update(self.item1, sold=True)
        create_order_status_code: tuple = create_order(request_order)[0]
        self.assertEqual(create_order_status_code, 400)


class ItemTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # create fake items
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.add_item_body = AddItemInput(ids=[1, 2, 3])
        # create fake items
        ItemRepository.create(
            name="item1",
            description="descr1",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=12.2,
        )
        self.item_to_search = ItemRepository.create(
            name="item2",
            description="descr2",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=9.2,
        )
        ItemRepository.create(
            name="item3",
            description="descr3",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=7.2,
        )

    def test_add_item_in_cart(self):
        self.client.login(username="testuser", password="testpassword")
        request_add_item = self.factory.post("/item/add")
        setattr(request_add_item, "user", self.user)
        add_item_status_code: tuple = add_item_in_cart(
            request_add_item, self.add_item_body
        )[0]
        self.assertEqual(add_item_status_code, 202)

    def test_search_for_item(self):
        response_body_expected: list = [
            {
                "id": 5,
                "name": "item2",
                "description": "descr2",
                "genre": "IT",
                "price": 9.2,
                "sold": False,
            }
        ]
        self.client.login(username="testuser", password="testpassword")
        request_search_item = self.factory.get("/item/search")
        setattr(request_search_item, "user", self.user)
        search_item_response: tuple = search_item(request_search_item, "item2")
        self.assertEqual(search_item_response[0], 202)
        search_item_body_response: list = search_item_response[1]
        self.assertEqual(
            len(search_item_body_response[0]), len(response_body_expected[0])
        )
        self.assertEqual(search_item_body_response[0], response_body_expected[0])
