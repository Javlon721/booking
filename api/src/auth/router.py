from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.db_queries import create_user, authenticate_user
from src.auth.models import Token
from src.auth.utils import create_access_token
from src.db.pool_dependency import ConnectionPoolDepends

user_auth_router = APIRouter(prefix="/auth")


@user_auth_router.post("/login")
def sing_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], conn_pool: ConnectionPoolDepends):
    user = authenticate_user(conn_pool, form_data)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token_data = {"sub": user.login, "user_id": user.user_id}
    access_token = create_access_token(token_data)

    return Token(access_token=access_token, token_type="bearer")


@user_auth_router.post("/signup")
def sing_up(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        conn_pool: ConnectionPoolDepends
):
    return create_user(conn_pool, form_data)
