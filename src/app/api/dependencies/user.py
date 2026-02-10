# Функция, которая создает сервис

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session_dep import SessionDep, TransactionSessionDep
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.user import UserService


async def get_user_service(
    session: Annotated[AsyncSession, SessionDep],
) -> UserService:
    repo = UserRepository(session, User)
    return UserService(session, repo)


async def get_user_service_tx(
    session: Annotated[AsyncSession, TransactionSessionDep],
) -> UserService:
    repo = UserRepository(session, User)
    return UserService(session, repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
UserServiceTxDep = Annotated[UserService, Depends(get_user_service_tx)]
