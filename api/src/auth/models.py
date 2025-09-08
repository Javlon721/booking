from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    user_id: Annotated[str, Field(min_length=7, max_length=100)]
    hashed_password: Annotated[str, Field(min_length=5, max_length=100, alias='password')]

    @staticmethod
    def indentify_by(user_id: str):
        return {'user_id': user_id}


@dataclass
class Token:
    access_token: str
    token_type: str


@dataclass
class TokenData:
    user_id: str | None = None
