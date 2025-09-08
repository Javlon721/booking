from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from pydantic import ValidationError

from src.auth.models import UserLogin
from src.auth.utils import verify_password, hash_password
from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.insert import insert_into
from src.db.sql_queries.select_actions import select_from_table
from src.db.sql_queries.utils import concat_sql_queries
from src.utils import list_dict_keys

USERS_LOGIN_TABLE = 'users_login'


def create_user(conn_pool: ConnectionPool, user_login: OAuth2PasswordRequestForm) -> UserLogin:
    user = UserLogin(user_id=user_login.username, password=hash_password(user_login.password))
    table_data = user.model_dump(by_alias=True)
    query = insert_into(USERS_LOGIN_TABLE, list_dict_keys(table_data))

    try:
        with conn_pool.connection() as conn:
            conn.row_factory = class_row(UserLogin)
            result: UserLogin = conn.execute(query, table_data).fetchone()

            return result
    except UniqueViolation as e:
        print(e)
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


def get_user_credentials(conn_pool: ConnectionPool, form_data: OAuth2PasswordRequestForm) -> UserLogin | None:
    indentify_by = UserLogin.indentify_by(form_data.username)
    query = concat_sql_queries(
        select_from_table(USERS_LOGIN_TABLE),
        add_and_conditions(list_dict_keys(indentify_by))
    )
    try:
        with conn_pool.connection() as conn:
            conn.row_factory = class_row(UserLogin)
            result = conn.execute(query, indentify_by).fetchone()

            if not result:
                return None

            return result
    except ValidationError as e:
        print(e)
        raise ValidationError("Parsing user info from user_login failed")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


def authenticate_user(conn_pool: ConnectionPool, form_data: OAuth2PasswordRequestForm) -> UserLogin | None:
    user_credentials = get_user_credentials(conn_pool, form_data)

    if not user_credentials:
        return None

    if not verify_password(form_data.password, user_credentials.hashed_password):
        return None

    return user_credentials
