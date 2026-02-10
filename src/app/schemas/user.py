from pydantic import BaseModel

from .mixins import (
    EmailMixin,
    FromAttributesMixin,
    FullNameMixin,
    IntIdMixin,
    PasswordMixin,
)


class UserBase(FullNameMixin, EmailMixin):
    pass


class UserRead(IntIdMixin, FromAttributesMixin):
    full_name: str
    email: str
    is_verified: bool = False
    role: str


class UserCreate(UserBase, PasswordMixin):
    pass


class UserCreateInternal(UserCreate):
    is_verified: bool = False


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None


class UserUpdateInternal(UserUpdate):
    is_verified: bool | None = None
