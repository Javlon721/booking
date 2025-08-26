from typing import Annotated

from fastapi import APIRouter, Body
from fastapi.security import OAuth2PasswordBearer

from src.auth.models import UserCreateInfo, UserLogin
from src.auth.utils import is_password_hashed

user_auth_router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@user_auth_router.post("/login")
def sing_in():
    return {"message": "Login"}


@user_auth_router.post("/signup")
def sing_up(user_login: Annotated[UserLogin, Body(alias="login")],
            user_info: Annotated[UserCreateInfo, Body(alias="info")]):
    return {
        "user_login": {
            "login": user_login.login,
            "password": user_login.hash_password,
            "is_hashed": is_password_hashed(user_login.hash_password),
        },
        "user_info": user_info.model_dump(exclude_unset=True)
    }
