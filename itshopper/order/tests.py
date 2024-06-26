from enum import StrEnum

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from .views import create_order
from .schemas import CreateOrderInput
from .models import Order


class OrderGenres(StrEnum):
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
        self.create_order_body = CreateOrderInput(ids=["1", "2", "3"])

        # create fake orders
        order1 = Order(name="Attrezzo", genre="", price=13.2)
        order2 = Order(
            name="Pasta termica", genre=OrderGenres.ORDER_GENRES_ELECTRONICS, price=3.2
        )
        order3 = Order(name="Mouse", genre=OrderGenres.ORDER_GENRES_IT, price=21)

    def test_order_made_successfully(self):
        self.client.login(username="testuser", password="testpassword")
        request_order = self.factory.post("/order/create")
        setattr(request_order, "user", self.user)
        create_order_status_code: tuple = create_order(
            request_order, self.create_order_body
        )[0]
        self.assertEqual(create_order_status_code, 202)
