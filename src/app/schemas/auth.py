from pydantic import BaseModel

from .mixins import PhoneNumberMixin


class LoginBase(BaseModel):
    password: str


class LoginWithPhone(LoginBase, PhoneNumberMixin):
    pass
