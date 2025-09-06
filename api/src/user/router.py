from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from psycopg.rows import class_row

from src.auth.dependencies import AuthorizeUserDepends
from src.auth.models import TokenData
from src.db.pool_dependency import ConnectionPoolDepends
from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.insert import insert_into
from src.db.sql_queries.select_actions import select_from_table
from src.db.sql_queries.update_action import update_row
from src.db.sql_queries.utils import concat_sql_queries
from src.user.models import UserCreateInfo, UserUpdateInfo, UserInfo
from src.utils import list_dict_keys

user_router = APIRouter(
    prefix="/user",
    tags=["user"])


@user_router.post("/create/info")
def create_new_user_info(
        user_info: Annotated[UserCreateInfo, Form()], conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    table, returning = 'users_info', "user_id"

    info = user_info.model_dump(exclude_unset=True, exclude_defaults=True)
    info.update({"user_id": token_data.user_id})

    query = insert_into(table, list_dict_keys(info), returning=[returning])

    try:
        with conn_pool.getconn() as conn:
            return conn.execute(query, info).fetchone()[0]
    except UniqueViolation:
        raise HTTPException(status_code=400, detail="User info already set")
    except ForeignKeyViolation:
        raise HTTPException(status_code=400, detail=f"User {token_data.user_id} doesn't exist")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


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


@user_router.get("/info/")
def create_new_user_info(
        conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    table, columns = 'users_info', '*'
    identify_user = {"user_id": token_data.user_id}
    query = concat_sql_queries(
        select_from_table(columns, table),
        add_and_conditions(list_dict_keys(identify_user))
    )
    try:
        with conn_pool.getconn() as conn:
            conn.row_factory = class_row(UserInfo)
            result: UserInfo = conn.execute(query, identify_user).fetchone()
            return result.model_dump(exclude_none=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
