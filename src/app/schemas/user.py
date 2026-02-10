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
    is_active: bool = True
    role: str


class UserCreate(UserBase, PasswordMixin):
    pass


class UserCreateInternal(UserCreate):
    is_active: bool = True


class UserUpdate(BaseModel):
    full_name: str | None = None


class UserUpdateInternal(UserUpdate):
    is_active: bool | None = None
