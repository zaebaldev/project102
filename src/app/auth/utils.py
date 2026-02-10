import uuid
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.security.private_key_path.read_text(),
    algorithm: str = settings.security.algorithm,
    expire_minutes: int = settings.security.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.security.public_key_path.read_text(),
    algorithm: str = settings.security.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode("utf-8")


def validate_password(
    password: str,
    hashed_password: bytes | str,
) -> bool:
    pwd_bytes: bytes = password.encode()
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode()
    return bcrypt.checkpw(
        password=pwd_bytes,
        hashed_password=hashed_password,
    )
