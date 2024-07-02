import json

from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja import Router
from ninja.security import django_auth

from setup_logs import setup_logging
from .logics import OrderLogic, BadRequest, ItemLogic
from .schemas import Response, AddItemInput

api = Router(tags=["order module"], auth=django_auth)
logger_console = setup_logging().getLogger("console")
logger_logstash = setup_logging().getLogger("logstash")


# Create your views here.
@api.post("/create", response={202: Response, 406: Response, 400: Response})
def create_order(request: HttpRequest):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested an order")
    logger_logstash.info(f"user {user} requested an order")
    try:
        logger_console.info(f"creating order for {user}")
        logger_logstash.info(f"creating order for {user}")
        OrderLogic.create_order_from_cart(user=user)
        return 202, Response(message="Order created")
    except BadRequest:
        logger_console.error("one or more items doesn't exists")
        logger_logstash.error("one or more items doesn't exists")
        return 400, Response(
            message="Order not made", errors="items with passed ids not present"
        )


# TODO add item, check orders, list items, ecc...
@api.post("/item/add", response={202: Response, 406: Response, 400: Response})
def add_item_in_cart(request: HttpRequest, data: AddItemInput):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested {data} in cart")
    logger_logstash.info(f"user {user} requested {data} in cart")
    try:
        ItemLogic.add_item_in_cart(data.ids, user)
        return 202, Response(message="Item added")
    except BadRequest:
        logger_console.error(f"one or more items doesn't exists")
        logger_logstash.error("one or more items doesn't exists")
        return 400, Response(
            message="Order not made", errors="items with passed ids not present"
        )


@api.get("/item/search", response={202: Response})
def search_item(request: HttpRequest, search_string: str):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested a research for {search_string}")
    logger_logstash.info(f"user {user} requested a research for {search_string}")
    result: list = ItemLogic.search_for_items(search_string)
    logger_console.info(f"items found {len(result)}")
    logger_logstash.info(f"items found {len(result)}")
    return 202, Response(message="Item added", body=json.dumps(result))
