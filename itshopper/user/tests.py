from django.test import TestCase, RequestFactory
from .views import register_user, login_user, logout_user
from .models import UserInput, LoginInput


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.register_body = UserInput(first_name="first_name",
                                       last_name="last_name",
                                       username="username",
                                       email="email@gmail.com",
                                       password="password")
        self.login_body = LoginInput(
            username="username",
            password="password"
        )

    def test_user_success_logout_as_user_logged_before(self):
        request_registration = self.factory.post("/user/register")
        registration_status_code: tuple = register_user(request_registration, self.register_body)[0]
        self.assertEqual(registration_status_code, 202)

        request_login = self.factory.post("/user/login")
        setattr(request_login, "session", self.client.session)
        login_status_code: tuple = login_user(request_login, self.login_body)[0]
        self.assertEqual(login_status_code, 202)

        request_logout = self.factory.post("/user/logout")
        setattr(request_logout, "session", self.client.session)
        logout_status_code: tuple = logout_user(request_logout)[0]
        self.assertEqual(logout_status_code, 202)

    def test_user_registration_failed_cause_already_exists(self):
        request_registration = self.factory.post("/user/register")
        registration_status_code: tuple = register_user(request_registration, self.register_body)[0]
        self.assertEqual(registration_status_code, 202)

        # repeat
        request_registration = self.factory.post("/user/register")
        registration_status_code: tuple = register_user(request_registration, self.register_body)[0]
        self.assertEqual(registration_status_code, 406)

    def test_user_login_success(self):
        request_registration = self.factory.post("/user/register")
        registration_status_code: tuple = register_user(request_registration, self.register_body)[0]
        self.assertEqual(registration_status_code, 202)

        request_login = self.factory.post("/user/login")
        setattr(request_login, "session", self.client.session)
        login_status_code: tuple = login_user(request_login, self.login_body)[0]
        self.assertEqual(login_status_code, 202)
