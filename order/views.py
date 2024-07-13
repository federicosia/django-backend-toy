from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.http import HttpRequest
from ninja import Router
from ninja.security import django_auth

from setup_logs import setup_logging
from .commands.comm_item import AddItemInCart, SearchItem
from .commands.comm_order import MakeOrder
from .schemas.item_schema import (
    AddItemInput,
    SearchItemOutput,
    AddItemOutput,
    AddItemException,
)
from .schemas.order_schema import CreateOrderInput, CreateOrderException

api = Router(tags=["order module"], auth=django_auth)
log_setup = setup_logging()
logger_console = log_setup.getLogger("console")
logger_logstash = log_setup.getLogger("logstash")


@api.post(
    "/create",
    response={
        202: CreateOrderInput,
        401: CreateOrderException,
        400: CreateOrderException,
    },
)
def create_order(request: HttpRequest):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested an order")
    logger_logstash.info(f"user {user} requested an order")
    try:
        logger_console.info(f"creating order for {user}")
        logger_logstash.info(f"creating order for {user}")
        order = MakeOrder(user).handle()
        return 202, order
    except BadRequest:
        logger_console.error(f"one or more items doesn't exists")
        logger_logstash.error("one or more items doesn't exists")
        return 400, {"message": f"one or more items in the oreder doesn't exists"}


# TODO add item, check orders, list items, ecc...
@api.post(
    "/item/add",
    response={202: AddItemOutput, 401: AddItemException, 400: AddItemException},
)
def add_item_in_cart(request: HttpRequest, data: AddItemInput):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested {data} in cart")
    logger_logstash.info(f"user {user} requested {data} in cart")
    try:
        user_cart = AddItemInCart(data.ids, user).handle()
        return 202, user_cart
    except BadRequest:
        logger_console.error(f"one or more items doesn't exists")
        logger_logstash.error("one or more items doesn't exists")
        return 400, {"message": f"one or more items with this {data} doesn't exists"}


@api.get("/item/search", response={202: SearchItemOutput})
def search_item(request: HttpRequest, search_string: str):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested a research for {search_string}")
    logger_logstash.info(f"user {user} requested a research for {search_string}")
    result: list = SearchItem(search_string).handle()
    logger_console.info(f"items found {len(result)}")
    logger_logstash.info(f"items found {len(result)}")
    return 202, result
