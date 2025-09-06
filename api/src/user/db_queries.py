from fastapi import HTTPException
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from psycopg_pool import ConnectionPool

from src.db.sql_queries.insert import insert_into
from src.user.models import UserCreateInfo
from src.utils import list_dict_keys


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
