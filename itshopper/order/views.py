from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja import Router
from ninja.security import django_auth

from setup_logs import setup_logging
from .logics import create_order_from_item_ids, BadRequest
from .schemas import CreateOrderInput, Response

api = Router(tags=["order module"], auth=django_auth)
logger_console = setup_logging().getLogger("console")
logger_logstash = setup_logging().getLogger("logstash")


# Create your views here.
@api.post("/create", response={202: Response, 406: Response, 400: Response})
def create_order(request: HttpRequest, data: CreateOrderInput):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested an order")
    logger_logstash.info(f"user {user} requested an order")
    try:
        logger_console.info(f"creating order for {user}")
        logger_logstash.info(f"creating order for {user}")
        create_order_from_item_ids(ids=data.ids, user=user)
        return 202, Response(message="Order created")
    except BadRequest:
        logger_console.error(f"one or more items doesn't exists")
        logger_logstash.error("one or more items doesn't exists")
        return 400, Response(
            message="Order not made", errors="items with passed ids not present"
        )
