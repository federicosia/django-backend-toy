from django.contrib.auth.models import User
from .models import UserInput, UserOutput
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login, logout
from ninja import Router

api = Router()


@api.post("/login")
def login_user(request: HttpRequest):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return f"Authenticated user {request.user}"
    else:
        return {"code": 500, "description": "NOT auth"}


@api.post("/logout")
def logout_user(request: HttpRequest):
    logout(request)
    return "user logged out"


@api.post("/register", response=UserOutput)
def register_user(request, user: UserInput):
    params: set = {"name", "surname", "username", "email", "password"}
    if params.issubset(request.POST):
        user = User.objects.create_user(
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            password=user.password,
        )
        return UserOutput(status_code=202, description="user created")
    else:
        print(f"{params} - {request.POST}")
        return {}
