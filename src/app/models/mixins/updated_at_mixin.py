from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from core.utils.get_current_date import get_current_dt


class UpdatedAtMixin:
    _updated_at_index: bool = False
    _updated_at_nullable: bool = False

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            index=cls._updated_at_index,
            default=None if cls._updated_at_nullable else get_current_dt,
            server_default=None if cls._updated_at_nullable else func.now(),
            onupdate=get_current_dt,
            nullable=cls._updated_at_nullable,
        )
