from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from src.auth.models import UserLogin, Token, TokenData, RefreshTokenData
from src.config import JWT_CONFIG
from src.utils import deep_copy

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def is_password_hashed(password: str) -> bool:
    return pwd_context.identify(password) is not None


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode: dict = deep_copy(data)
    default_time_delta = timedelta(minutes=JWT_CONFIG.access_token_expire_minutes)

    if not expires_delta:
        expire = datetime.now(timezone.utc) + default_time_delta
    else:
        expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    result = jwt.encode(to_encode, JWT_CONFIG.secret_key, algorithm=JWT_CONFIG.algorithm)

    return result


def create_refresh_token(data: dict[str, Any]) -> str:
    return create_access_token(data, expires_delta=timedelta(hours=JWT_CONFIG.refresh_token_expire_hours))


def create_user_tokens(user: UserLogin) -> Token:
    token_data = TokenData(user_id=user.user_id).model_dump()
    refresh_token_data = RefreshTokenData(user_id=user.user_id, refresh=True).model_dump()

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(refresh_token_data)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, JWT_CONFIG.secret_key, algorithms=[JWT_CONFIG.algorithm])
