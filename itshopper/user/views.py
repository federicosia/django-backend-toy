from django.contrib.auth.models import User
from .models import Response, UserInput, LoginInput
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login, logout
from ninja import Router

api = Router()


@api.post("/login", response={202: Response, 406: Response})
def login_user(request: HttpRequest, data: LoginInput):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        return 202, Response(message="User logged in")
    else:
        return 406, Response(
            message="User not logged in", errors="User does not exists"
        )


@api.post("/logout", response={202: Response})
def logout_user(request: HttpRequest):
    logout(request)
    return 202, Response(message="User logged out")


@api.post("/register", response={202: Response, 406: Response})
def register_user(request, data: UserInput):
    if not User.objects.filter(username=data.username):
        User.objects.create_user(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            email=data.email,
            password=data.password,
        )
        return 202, Response(message="user created")
    else:
        return 406, Response(message="user already registered")
