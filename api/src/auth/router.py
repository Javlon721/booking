from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.auth.db_queries import create_user, add_new_user_info, authenticate_user
from src.auth.models import UserCreateInfo, UserLogin, Token
from src.auth.utils import create_access_token
from src.db.pool_dependency import ConnectionPoolDepends

user_auth_router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@user_auth_router.post("/login")
def sing_in(user_login: Annotated[UserLogin, Form()], conn_pool: ConnectionPoolDepends):
    user = authenticate_user(conn_pool, user_login)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token_data = {"sub": user.login}
    access_token = create_access_token(token_data)

    return Token(access_token=access_token, token_type="bearer")


@user_auth_router.post("/signup")
def sing_up(
        user_login: Annotated[UserLogin, Form()],
        conn_pool: ConnectionPoolDepends
):
    return create_user(conn_pool, user_login)


@user_auth_router.post("/signup/user_info/{user_id}")
def create_new_user_info(
        user_id: int,
        user_info: Annotated[UserCreateInfo, Form()], conn_pool: ConnectionPoolDepends):
    return add_new_user_info(conn_pool, user_id, user_info)
