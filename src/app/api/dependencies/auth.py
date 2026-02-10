from typing import Annotated, Callable

from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.user import UserServiceDep
from app.auth.helpers import ACCESS_TOKEN_TYPE
from app.auth.validation import (
    get_current_token_payload_from_header,
    validate_token_type,
)
from app.db.session_dep import SessionDep, TransactionSessionDep
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRead
from app.services.auth import AuthService
from core.enums.roles import RolesEnum
from core.exceptions import AuthenticationError, PermissionDeniedError

http_bearer = HTTPBearer(auto_error=False)


async def get_auth_service(
    session: Annotated[AsyncSession, SessionDep],
) -> AuthService:
    user_repo = UserRepository(session, User)
    return AuthService(
        session=session,
        user_repo=user_repo,
    )


async def get_auth_service_tx(
    session: Annotated[AsyncSession, TransactionSessionDep],
) -> AuthService:
    user_repo = UserRepository(session, User)
    return AuthService(
        session=session,
        user_repo=user_repo,
    )


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
AuthServiceTxDep = Annotated[AuthService, Depends(get_auth_service_tx)]


def get_auth_user_from_token_type(token_type: str) -> Callable:
    async def get_auth_user(
        user_service: UserServiceDep,
        payload: dict = Depends(get_current_token_payload_from_header),
    ) -> User:
        validate_token_type(payload, token_type)
        subject_id = payload.get("sub")
        if subject_id is None:
            raise AuthenticationError(
                message="Invalid token (subject not found)",
            )
        user = await user_service.get_by_id(int(subject_id))
        if user:
            return user

    return get_auth_user


get_current_auth_user = get_auth_user_from_token_type(ACCESS_TOKEN_TYPE)


CurrentUserDep = Annotated[UserRead, Depends(get_current_auth_user)]


async def get_current_auth_admin(
    current_auth_user: CurrentUserDep,
) -> User:
    if current_auth_user.role != RolesEnum.ADMIN.value:
        raise PermissionDeniedError(
            message="You are not authorized to perform this action",
        )
    return current_auth_user


CurrentAdminDep = Annotated[UserRead, Depends(get_current_auth_admin)]
