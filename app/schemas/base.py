from email_validator import EmailNotValidError
from email_validator import validate_email as validate_e
from pydantic import BaseModel


class EmailField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> str:
        try:
            validate_e(v)
            return v
        except EmailNotValidError:
            raise ValueError("Not valid email")


class BaseUser(BaseModel):
    email: EmailField


class BaseComplaint(BaseModel):
    title: str
    description: str
    amount: float
