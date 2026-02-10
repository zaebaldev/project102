from datetime import timedelta

from app.auth import utils as auth_utils
from core.config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.security.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(
    subject: str,
    role: str,
) -> str:
    jwt_payload = {
        "sub": subject,
        "role": role,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.security.access_token_expire_minutes,
    )


def create_refresh_token(
    subject: str,
    role: str,
) -> str:
    jwt_payload = {
        "sub": subject,
        "role": role,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.security.refresh_token_expire_days),
    )
