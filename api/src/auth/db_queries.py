from fastapi import HTTPException
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from psycopg.sql import SQL, Placeholder, Identifier
from psycopg_pool import ConnectionPool

from src.auth.models import UserLogin, UserCreateInfo


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
