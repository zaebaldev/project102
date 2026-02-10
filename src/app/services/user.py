from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from core.exceptions import NotFoundError


class UserService:
    """Service for user-related business logic."""

    def __init__(
        self,
        session: AsyncSession,
        repo: UserRepository,
    ):
        self.session = session
        self.repo = repo

    async def get_by_id(
        self,
        user_id: int,
    ) -> "User":
        user = await self.repo.get_by_id(id=user_id)
        if not user:
            raise NotFoundError(
                message="User not found",
            )
        return user

    async def get_by_phone(
        self,
        phone_number: str,
    ) -> "User":
        user = await self.repo.get_by_phone(phone_number)
        if not user:
            raise NotFoundError(
                message="User not found",
            )
        return user

    async def delete_user(
        self,
        user_id: int,
    ) -> None:
        await self.repo.delete_by_id(user_id)

    async def get_all_users(self) -> list[Optional["User"]]:
        return await self.repo.get_all()

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> "User":
        user = await self.repo.get_by_id(id=user_id)
        if not user:
            raise NotFoundError(
                message="User not found",
            )
        return user
