from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    user_id: Annotated[int, Field(gt=0)]
    login: Annotated[str, Field(min_length=7, max_length=100)]
    hashed_password: Annotated[str, Field(min_length=5, max_length=100, alias='password')]


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


@dataclass
class Token:
    access_token: str
    token_type: str
