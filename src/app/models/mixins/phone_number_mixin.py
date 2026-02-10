from sqlalchemy import String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class PhoneNumberMixin:
    _phone_number_nullable: bool = False
    _phone_number_unique: bool = False
    _phone_number_index = False

    @declared_attr
    def phone_number(cls) -> Mapped[str]:
        return mapped_column(
            String(255),
            unique=cls._phone_number_unique,
            nullable=cls._phone_number_nullable,
            index=cls._phone_number_index,
        )
