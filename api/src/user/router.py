from typing import Annotated

from fastapi import APIRouter, Form, HTTPException

from src.auth.dependencies import AuthorizeUserDepends
from src.auth.models import TokenData
from src.db.pool_dependency import ConnectionPoolDepends
from src.db.sql_queries.update_action import update_row
from src.user.db_queries import add_new_user_info
from src.user.models import UserCreateInfo, UserUpdateInfo
from src.utils import list_dict_keys

user_router = APIRouter(
    prefix="/user",
    tags=["user"])


@user_router.post("/create/info")
def create_new_user_info(
        user_info: Annotated[UserCreateInfo, Form()], conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    return add_new_user_info(conn_pool, token_data.user_id, user_info)


@user_router.put("/update/info/")
def create_new_user_info(
        user_info: Annotated[UserUpdateInfo, Form()], conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    table, returning = 'users_info', "user_id"

    identify_user = {"user_id": token_data.user_id}
    info = user_info.model_dump(exclude_none=True)

    query = update_row(list_dict_keys(info), list_dict_keys(identify_user), table, returning=[returning])
    info.update(identify_user)

    try:
        with conn_pool.getconn() as conn:
            return conn.execute(query, info).fetchone()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
