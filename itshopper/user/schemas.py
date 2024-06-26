from typing import Optional

from ninja import Schema


class LoginInput(Schema):
    username: str
    password: str


class UserInput(Schema):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class Response(Schema):
    message: str
    errors: Optional[str] = None
