from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja import Router
from ninja.security import django_auth

from setup_logs import setup_logging
from .schemas import CreateOrderInput, Response

api = Router(tags=["order module"], auth=django_auth)
logger_console = setup_logging().getLogger("console")
logger_logstash = setup_logging().getLogger("logstash")


# Create your views here.
@api.post("/create")
def create_order(request: HttpRequest, data: CreateOrderInput):
    user: User = getattr(request, "user", None)
    logger_console.info(f"user {user} requested an order")
    if user.is_authenticated:
        return "you are creating an order"
    else:
        return 406, Response(
            message="User not logged in", errors="User does not exists"
        )
