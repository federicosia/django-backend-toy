from typing import List, Optional
from ninja import Schema, ModelSchema

from order.models import Item


class CreateOrderInput(Schema):
    ids: List[int]


class CreateItemInput(ModelSchema):
    class Meta:
        model = Item
        fields = "__all__"


class Response(Schema):
    message: str
    errors: Optional[str] = None
