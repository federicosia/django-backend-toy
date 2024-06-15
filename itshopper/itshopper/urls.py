from django.contrib import admin
from django.urls import path
from order.views import api as order_api
from user.views import api as user_api
from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("user/", user_api)
api.add_router("order/", order_api)


urlpatterns = [
    path("", api.urls),
    path("admin/", admin.site.urls),
]
