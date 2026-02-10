from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from core.utils.get_current_date import get_current_dt


class CreatedAtMixin:
    _created_at_index: bool = False
    _created_at_nullable: bool = False

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            index=cls._created_at_index,
            default=get_current_dt,
            server_default=func.now(),
            nullable=cls._created_at_nullable,
        )
