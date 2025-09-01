from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from pydantic import ValidationError

from src.auth.models import UserLogin, UserCreateInfo
from src.auth.utils import verify_password, hash_password
from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.insert import insert_into
from src.db.sql_queries.select_actions import select_from_table
from src.db.sql_queries.utils import concat_sql_queries
from src.utils import list_dict_keys


def create_user(conn_pool: ConnectionPool, user_login: OAuth2PasswordRequestForm) -> int:
    table, returning = 'users_login', "user_id"
    table_data = {
        "login": user_login.username,
        "password": hash_password(user_login.password),
    }
    query = insert_into(table, list_dict_keys(table_data), returning)

    try:
        with conn_pool.getconn() as conn:
            return conn.execute(query, table_data).fetchone()[0]
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


def get_user_login_info(conn_pool: ConnectionPool, form_data: OAuth2PasswordRequestForm) -> UserLogin | None:
    table, pool_columns = 'users_login', "*"
    indentify_by = {"login": form_data.username, }
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
    except ValidationError:
        raise ValidationError("Parsing user info from user_login failed")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def authenticate_user(conn_pool: ConnectionPool, form_data: OAuth2PasswordRequestForm) -> UserLogin | None:
    user_credentials = get_user_login_info(conn_pool, form_data)

    if not user_credentials:
        return None

    if not verify_password(form_data.password, user_credentials.hashed_password):
        return None

    return user_credentials
