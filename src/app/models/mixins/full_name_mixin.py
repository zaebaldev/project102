from sqlalchemy import String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class FullNameMixin:
    _full_name_nullable: bool = False
    _full_name_unique: bool = False

    @declared_attr
    def full_name(cls) -> Mapped[str]:
        return mapped_column(
            String(512),
            unique=cls._full_name_unique,
            nullable=cls._full_name_nullable,
        )
