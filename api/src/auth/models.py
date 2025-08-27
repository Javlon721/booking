from datetime import datetime, date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from src.auth.utils import hash_password, is_password_hashed


class UserLogin(BaseModel):
    login: Annotated[str, Field(min_length=7, max_length=100)]
    password: Annotated[str, Field(min_length=5, max_length=100)]

    @property
    def hash_password(self) -> str:
        if not is_password_hashed(self.password):
            return hash_password(self.password)
        return self.password

    def identifications(self) -> dict:
        return {
            'login': self.login,
        }


class UserCreateInfo(BaseModel):
    first_name: Annotated[str, Field(min_length=2)]
    last_name: str | None = None
    date_of_birth: date
    phone: Annotated[str, Field(min_length=9, max_length=9)]


class UserInfo(UserCreateInfo):
    user_id: int
    created_at: datetime
    customer_wallet: Decimal
    admin_wallet: Decimal
