from typing import TYPE_CHECKING, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.helpers import (
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
)
from app.auth.utils import hash_password, validate_password
from app.auth.validation import get_token_payload, validate_token_type
from app.repositories.user import UserRepository
from app.schemas.auth import LoginWithPhone
from app.schemas.token import RefreshToken, TokenInfo
from app.schemas.user import UserCreate
from core.exceptions import AlreadyExistsError
from core.exceptions.common import AuthenticationError

if TYPE_CHECKING:
    from app.models.user import User


class AuthService:
    """Service for authentication."""

    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
    ):
        self.session = session
        self.user_repo = user_repo

    async def register_new_user(
        self,
        user_data: UserCreate,
    ) -> "User":
        existing_user = await self.user_repo.get_by_phone(user_data.phone_number)
        if existing_user:
            raise AlreadyExistsError(
                message="User already registered",
            )
        hashed_password = hash_password(user_data.password)
        user = await self.user_repo.create(
            phone_number=user_data.phone_number,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )
        return user

    async def authenticate(
        self,
        phone_number: str,
        password: str,
    ) -> Optional[tuple["User", str]]:
        user = await self.user_repo.get_by_phone(phone_number=phone_number)
        if user:
            if validate_password(password, user.hashed_password):
                return user, user.role
        return None

    async def login(
        self,
        login_data: LoginWithPhone,
    ) -> TokenInfo:
        result = await self.authenticate(
            phone_number=login_data.phone_number,
            password=login_data.password,
        )
        if result is None:
            raise AuthenticationError(message="Invalid phone or password")
        user_entity, role = result
        access_token = create_access_token(str(user_entity.id), role=role)
        refresh_token = create_refresh_token(str(user_entity.id), role=role)
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_token(
        self,
        refresh_token_data: RefreshToken,
    ) -> TokenInfo:
        token = refresh_token_data.refresh_token

        if not token:
            raise AuthenticationError(
                message="Refresh token is missing",
            )
        payload = get_token_payload(token=token)
        validate_token_type(payload, REFRESH_TOKEN_TYPE)
        subject_id = payload.get("sub")
        if subject_id is None:
            raise AuthenticationError(
                message="Invalid token (subject not found)",
            )
        user = await self.user_repo.get_by_id(int(subject_id))
        if user is None:
            raise AuthenticationError(
                message="Invalid token (user not found)",
            )
        new_access_token = create_access_token(
            subject=str(user.id),
            role=payload.get("role"),
        )
        return TokenInfo(
            access_token=new_access_token,
        )
