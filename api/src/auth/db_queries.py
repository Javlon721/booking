from fastapi import HTTPException
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from psycopg.rows import class_row
from psycopg.sql import SQL, Placeholder, Identifier
from psycopg_pool import ConnectionPool

from src.auth.models import UserLogin, UserCreateInfo
from src.auth.utils import verify_password
from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.select_actions import select_from_table
from src.db.sql_queries.utils import concat_sql_queries
from src.utils import list_dict_keys


def create_user(conn_pool: ConnectionPool, user_login: UserLogin):
    query = SQL("insert into users_login (login, password) values (%s, %s) returning user_id")
    try:
        with conn_pool.getconn() as conn:
            return conn.execute(query, (user_login.login, user_login.hash_password)).fetchone()[0]
    except UniqueViolation:
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def add_new_user_info(conn_pool: ConnectionPool, user_id: int, user_info: UserCreateInfo):
    info = user_info.model_dump(exclude_unset=True, exclude_defaults=True)
    info.update({"user_id": user_id})

    set_columns = info.keys()
    query = SQL("insert into users_info ({columns}) values ({values}) returning user_id").format(
        columns=SQL(', ').join(map(Identifier, set_columns)),
        values=SQL(', ').join(map(Placeholder, set_columns))
    )
    try:
        with conn_pool.getconn() as conn:
            return conn.execute(query, info).fetchone()[0]
    except UniqueViolation:
        raise HTTPException(status_code=400, detail="User info already set")
    except ForeignKeyViolation:
        raise HTTPException(status_code=400, detail=f"User {user_id} doesn't exist")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def get_user_login_info(conn_pool: ConnectionPool, user_login: UserLogin) -> UserLogin:
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
            return conn.execute(query, indentify_by).fetchone()
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


def authenticate_user(conn_pool: ConnectionPool, user_login: UserLogin):
    user_credentials = get_user_login_info(conn_pool, user_login)
    if not verify_password(user_login.password, user_credentials.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    return user_credentials


def get_user_credentials(conn_pool: ConnectionPool, user_login: UserLogin):
    user = authenticate_user(conn_pool, user_login)
    return user
