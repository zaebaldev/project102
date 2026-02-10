from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role

from .base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[Role],
    ):
        super().__init__(session, model)
