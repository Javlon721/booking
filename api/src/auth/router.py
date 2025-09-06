from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.db_queries import create_user, authenticate_user
from src.auth.utils import create_user_tokens
from src.db.pool_dependency import ConnectionPoolDepends

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login")
def sing_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], conn_pool: ConnectionPoolDepends):
    user = authenticate_user(conn_pool, form_data)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    tokens = create_user_tokens(user)
    return tokens


@auth_router.post("/signup")
def sing_up(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        conn_pool: ConnectionPoolDepends
):
    return create_user(conn_pool, form_data)
