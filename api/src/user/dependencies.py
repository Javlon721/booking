from typing import Annotated, Callable

from fastapi import HTTPException

from src.auth.dependencies import AuthorizeUserDepends
from src.auth.models import TokenData, UserLogin
from src.db.pool_dependency import ConnectionPoolDepends
from src.db.sql_queries.delete_actions import delete_row
from src.utils import list_dict_keys


def delete_user_data(table: str, returning: str | None = None) -> Callable:
    def delete_user_dependence(conn_pool: ConnectionPoolDepends,
                               token_data: Annotated[TokenData, AuthorizeUserDepends]):
        identify_user = UserLogin.indentify_by(token_data.user_id)
        query = delete_row(list_dict_keys(identify_user), table, returning=[returning])

        try:
            with conn_pool.connection() as conn:
                return conn.execute(query, identify_user).fetchone()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Something went wrong")

    return delete_user_dependence
