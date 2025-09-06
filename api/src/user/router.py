from typing import Annotated

from fastapi import APIRouter, Form

from src.auth.dependencies import AuthorizeUserDepends
from src.auth.models import TokenData
from src.db.pool_dependency import ConnectionPoolDepends
from src.user.db_queries import add_new_user_info
from src.user.models import UserCreateInfo

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[AuthorizeUserDepends]
)


@user_router.post("/create/info")
def create_new_user_info(
        user_info: Annotated[UserCreateInfo, Form()], conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    return add_new_user_info(conn_pool, token_data.user_id, user_info)
