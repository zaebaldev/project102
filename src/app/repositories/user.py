from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[User],
    ):
        super().__init__(session, model)

    async def get_by_phone(
        self,
        phone_number: str,
    ) -> User | None:
        """Get user by phone."""
        result = await self.find_one(
            filters=[
                User.phone_number == phone_number,
            ],
        )
        return result

    async def create(
        self,
        phone_number: str,
        hashed_password: str,
        full_name: str,
    ) -> User:
        """Create a new user."""
        return await self.add(
            instance=User(
                phone_number=phone_number,
                hashed_password=hashed_password,
                full_name=full_name,
            ),
        )
