from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    user_id: Annotated[str, Field(min_length=7, max_length=100)]
    hashed_password: Annotated[str, Field(min_length=5, max_length=100, alias='password')]


@dataclass
class Token:
    access_token: str
    token_type: str


@dataclass
class TokenData:
    user_id: int | None = None
