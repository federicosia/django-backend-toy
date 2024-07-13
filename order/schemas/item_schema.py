from typing import List

from django.core.exceptions import BadRequest, PermissionDenied
from ninja import Schema, ModelSchema

from order.models import Item, Cart


class AddItemInput(Schema):
    ids: List[int]


class AddItemException(Schema):
    message: str


class CreateItemInput(ModelSchema):
    class Meta:
        model = Item
        fields = "__all__"


class AddItemOutput(ModelSchema):
    class Meta:
        model = Cart
        fields = "__all__"


class SearchItemOutput(ModelSchema):
    class Meta:
        model = Item
        fields = "__all__"
