from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app.auth import utils as auth_utils

from .helpers import TOKEN_TYPE_FIELD

http_bearer = HTTPBearer(auto_error=False)


def get_token_payload(token: str) -> dict:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )
    return payload


def get_current_token_payload_from_header(
    auth_token: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = auth_token.credentials if auth_token else None
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return get_token_payload(token=token)


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )
