from sqlalchemy import String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class EmailMixin:
    _email_nullable: bool = False
    _email_unique: bool = False

    @declared_attr
    def email(cls) -> Mapped[str]:
        return mapped_column(
            String(512),
            unique=cls._email_unique,
            nullable=cls._email_nullable,
        )
