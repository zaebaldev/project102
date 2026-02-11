import logging

from fastapi import (
    APIRouter,
    Request,
    status,
)

from app.api.dependencies.auth import AuthServiceDep, AuthServiceTxDep
from app.rate_limiter import get_default_rate_limit, limiter
from app.schemas.auth import LoginWithPhone
from app.schemas.token import RefreshToken, TokenInfo
from app.schemas.user import UserCreate, UserRead
from core.config import settings

log = logging.getLogger(__name__)
router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)


@router.post(
    "/signup",
    summary="Register new user",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    description="""
    Creates a new user account with the provided information.
    """,
    responses={
        status.HTTP_201_CREATED: {
            "description": "User successfully registered",
            "model": UserRead,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Invalid input data or user already exists",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User already exists",
                        "details": None,
                    }
                }
            },
        },
    },
)
async def register(
    user_data: UserCreate,
    auth_service: AuthServiceTxDep,
):
    """Register a new user with the provided details."""
    return await auth_service.register_new_user(user_data)


@router.post(
    "/login",
    summary="Login user",
    response_model=TokenInfo,
    description="""
    Authenticates a user and returns JWT tokens.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully authenticated",
            "model": TokenInfo,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect phone or password",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid phone or password",
                        "details": None,
                    }
                }
            },
        },
    },
)
@limiter.limit(get_default_rate_limit())
async def login(
    request: Request,
    auth_service: AuthServiceTxDep,
    login_data: LoginWithPhone,
):
    """Login a user with the provided phone and password."""
    return await auth_service.login(login_data)


@router.post(
    "/refresh",
    summary="Get new access token",
    response_model=TokenInfo,
    description="""
    Refreshes an access token using a refresh token.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully refreshed token",
            "model": TokenInfo,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid refresh token",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid token",
                        "details": None,
                    }
                }
            },
        },
    },
)
async def refresh(
    token_data: RefreshToken,
    auth_service: AuthServiceDep,
):
    """Refresh an access token using a refresh token."""
    return await auth_service.refresh_token(token_data)
