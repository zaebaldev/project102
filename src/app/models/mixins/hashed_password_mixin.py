from sqlalchemy import String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class HashedPasswordMixin:
    @declared_attr
    def hashed_password(cls) -> Mapped[str]:
        return mapped_column(String(512))
