from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.utils import SetNonesMixin


class UserCreateInfo(BaseModel):
    first_name: str | None = Field(min_length=2)
    last_name: str | None = None
    date_of_birth: date | None
    phone: str | None = Field(min_length=9, max_length=9)


class UserUpdateInfo(UserCreateInfo, SetNonesMixin):
    pass


class UserInfo(UserCreateInfo):
    user_id: str
    created_at: datetime
    customer_wallet: Decimal = Field(ge=0)
    admin_wallet: Decimal = Field(ge=0)

    @staticmethod
    def foreign_key(value: str):
        return {'user_id': value}
