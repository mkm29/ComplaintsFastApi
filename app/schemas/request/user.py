from ..base import BaseUser


class RegisterUserIn(BaseUser):
    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str


class LoginUserIn(BaseUser):
    password: str
