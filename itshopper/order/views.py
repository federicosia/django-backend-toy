from ninja import Router
from ninja.security import django_auth

api = Router()


# Create your views here.
@api.post("/create", auth=django_auth)
def create_order(request):
    return "you are creating an order"
