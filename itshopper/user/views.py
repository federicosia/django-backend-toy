from .repositories.users import UserRepository
from .schemas import Response, UserInput, LoginInput
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login, logout
from setup_logs import setup_logging
from ninja import Router

api = Router(tags=["user module"])
logger_console = setup_logging().getLogger("console")
logger_logstash = setup_logging().getLogger("logstash")


@api.post("/login", response={202: Response, 406: Response})
def login_user(request: HttpRequest, data: LoginInput):
    logger_console.info(f"Authenticating user {data}")
    logger_logstash.info(f"Authenticating user {data}")
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        logger_console.info(f"Authenticated successfully")
        logger_logstash.info(f"Authenticated successfully")
        return 202, Response(message="User logged in")
    else:
        logger_console.info(f"Authentication failed")
        logger_logstash.info(f"Authentication failed")
        return 406, Response(
            message="User not logged in", errors="User does not exists"
        )


@api.post("/logout", response={202: Response})
def logout_user(request: HttpRequest):
    logger_console.info(f"User requested logout {getattr(request, "user", None)}")
    logger_logstash.info(f"User requested logout {getattr(request, "user", None)}")
    logout(request)
    return 202, Response(message="User logged out")


@api.post("/register", response={202: Response, 406: Response})
def register_user(request: HttpRequest, data: UserInput):
    logger_console.info(f"Registering an user {data}")
    logger_logstash.info(f"Registering an user {data}")
    if not UserRepository.filter(username=data.username):
        UserRepository.create(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            email=data.email,
            password=data.password,
        )
        logger_console.info(f"Registered user {data.username} successfully")
        logger_logstash.info(f"Registered user {data.username} successfully")
        return 202, Response(message="user created")
    else:
        logger_console.info(f"User {data.username} already exists")
        logger_logstash.info(f"User {data.username} already exists")
        return 406, Response(message="user already registered")
