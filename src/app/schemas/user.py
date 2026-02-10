from pydantic import BaseModel

from .mixins import (
    FromAttributesMixin,
    FullNameMixin,
    IntIdMixin,
    PasswordMixin,
    PhoneNumberMixin,
)


class UserBase(FullNameMixin, PhoneNumberMixin):
    pass


class UserRead(IntIdMixin, FromAttributesMixin):
    full_name: str
    phone_number: str
    is_verified: bool = False
    role: str


class UserCreate(UserBase, PasswordMixin):
    pass


class UserCreateInternal(UserCreate):
    is_verified: bool = False


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None


class UserUpdateInternal(UserUpdate):
    is_verified: bool | None = None
