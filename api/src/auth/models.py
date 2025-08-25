from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    login: Annotated[str, Field(min_length=7, max_length=100)]
    password: Annotated[str, Field(min_length=5, max_length=100)]


class UserCreateInfo(BaseModel):
    first_name: Annotated[str, Field(min_length=2)]
    last_name: str | None = None
    phone: Annotated[str, Field(min_length=9, max_length=9)]


class UserInfo(UserCreateInfo):
    user_id: int
    created_at: datetime
    customer_wallet: Decimal
    admin_wallet: Decimal
