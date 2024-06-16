from ninja import Router
from ninja.security import django_auth

api = Router(tags=["order module"], auth=django_auth)


# Create your views here.
@api.post("/create")
def create_order(request):
    return "you are creating an order"
