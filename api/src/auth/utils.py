from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from src.auth.models import UserLogin, Token
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


def create_user_tokens(user: UserLogin):
    token_data = {"sub": user.user_id}
    access_token = create_access_token(token_data)

    return Token(access_token=access_token, token_type="bearer")
