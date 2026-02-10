from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import (
    CreatedAtMixin,
    FullNameMixin,
    HashedPasswordMixin,
    IntIdMixin,
    PhoneNumberMixin,
    UpdatedAtMixin,
)


class User(
    Base,
    IntIdMixin,
    FullNameMixin,
    HashedPasswordMixin,
    PhoneNumberMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
):
    _id_autoincrement = True
    _id_primary_key = True
    _phone_number_unique = True
    _phone_number_index = True
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    role: Mapped[str] = mapped_column(
        ForeignKey("roles.name"),
        default="user",
        server_default="user",
    )
