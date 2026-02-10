from sqlalchemy import String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class NameMixin:
    _name_nullable: bool = False
    _name_unique: bool = False
    _name_primary_key: bool = True

    @declared_attr
    def name(cls) -> Mapped[str]:
        return mapped_column(
            String(512),
            unique=cls._name_unique,
            nullable=cls._name_nullable,
            primary_key=cls._name_primary_key,
        )
