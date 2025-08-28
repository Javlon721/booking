from fastapi import HTTPException
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool

from src.auth.models import UserLogin, UserCreateInfo
from src.auth.utils import verify_password
from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.insert import insert_into
from src.db.sql_queries.select_actions import select_from_table
from src.db.sql_queries.utils import concat_sql_queries
from src.utils import list_dict_keys


def create_user(conn_pool: ConnectionPool, user_login: UserLogin) -> int:
    table, returning = 'users_login', "user_id"
    data = user_login.db_data()
    new_query = insert_into(table, list_dict_keys(data), returning)

    try:
        with conn_pool.getconn() as conn:
            return conn.execute(new_query, data).fetchone()[0]
    except UniqueViolation:
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def add_new_user_info(conn_pool: ConnectionPool, user_id: int, user_info: UserCreateInfo):
    table, returning = 'users_info', "user_id"
    info = user_info.model_dump(exclude_unset=True, exclude_defaults=True)
    info.update({"user_id": user_id})
    query = insert_into(table, list_dict_keys(info), returning)

    try:
        with conn_pool.getconn() as conn:
            return conn.execute(query, info).fetchone()[0]
    except UniqueViolation:
        raise HTTPException(status_code=400, detail="User info already set")
    except ForeignKeyViolation:
        raise HTTPException(status_code=400, detail=f"User {user_id} doesn't exist")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def get_user_login_info(conn_pool: ConnectionPool, user_login: UserLogin) -> UserLogin | None:
    table = 'users_login'
    indentify_by = user_login.identifications()
    pool_columns = "*"
    query = concat_sql_queries(
        select_from_table(pool_columns, table),
        add_and_conditions(list_dict_keys(indentify_by))
    )
    try:
        with conn_pool.getconn() as conn:
            conn.row_factory = class_row(UserLogin)
            result = conn.execute(query, indentify_by).fetchone()

            if not result:
                return None

            return result
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def authenticate_user(conn_pool: ConnectionPool, user_login: UserLogin) -> UserLogin | None:
    user_credentials = get_user_login_info(conn_pool, user_login)

    if not user_credentials:
        return None

    if not verify_password(user_login.password, user_credentials.password):
        return None

    return user_credentials


def get_user_credentials(conn_pool: ConnectionPool, user_login: UserLogin):
    user = authenticate_user(conn_pool, user_login)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return user
