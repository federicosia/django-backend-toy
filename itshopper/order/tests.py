from enum import StrEnum

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from .views import create_order
from .schemas import CreateOrderInput
from .repositories.items import ItemRepository


class ItemGenres(StrEnum):
    ORDER_GENRES_IT = "IT"
    ORDER_GENRES_ELECTRONICS = "EL"
    ORDER_GENRES_TMP = "TM"


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.create_order_body = CreateOrderInput(ids=[1, 2, 3])
        self.create_order_body_bad = CreateOrderInput(ids=[1, 222, 3])

        # create fake items
        ItemRepository.create(
            name="item1",
            description="descr1",
            genre=ItemGenres.ORDER_GENRES_IT,
            price=12.2,
        )
        ItemRepository.create(
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

    def test_create_order_made_successfully(self):
        self.client.login(username="testuser", password="testpassword")
        request_order = self.factory.post("/order/create")
        setattr(request_order, "user", self.user)
        create_order_status_code: tuple = create_order(
            request_order, self.create_order_body
        )[0]
        self.assertEqual(create_order_status_code, 202)

    def test_create_order_made_unsuccessfully(self):
        self.client.login(username="testuser", password="testpassword")
        request_order = self.factory.post("/order/create")
        setattr(request_order, "user", self.user)
        create_order_status_code: tuple = create_order(
            request_order, self.create_order_body_bad
        )[0]
        self.assertEqual(create_order_status_code, 400)
