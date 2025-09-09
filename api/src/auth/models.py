from typing import Annotated

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    user_id: Annotated[str, Field(min_length=7, max_length=100)]
    hashed_password: Annotated[str, Field(min_length=5, max_length=100, alias='password')]

    @staticmethod
    def indentify_by(user_id: str):
        return {'user_id': user_id}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None
