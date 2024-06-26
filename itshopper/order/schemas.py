from typing import List, Optional
from ninja import Schema, ModelSchema


class CreateOrderInput(Schema):
    ids: List[str]


class Response(Schema):
    message: str
    errors: Optional[str] = None
