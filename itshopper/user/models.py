from ninja import Schema


class UserInput(Schema):
    name: str
    surname: str
    username: str
    email: str
    password: str


class UserOutput(Schema):
    status_code: int
    description: str
    email: str
