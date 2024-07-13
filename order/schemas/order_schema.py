from ninja import Schema


class CreateOrderInput(Schema):
    cart_id: int
    user_id: int


class CreateOrderException(Schema):
    message: str
