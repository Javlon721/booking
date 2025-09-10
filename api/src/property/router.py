from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from src.auth.dependencies import AuthorizeUserDepends
from src.auth.models import TokenData
from src.db.pool_dependency import ConnectionPoolDepends
from src.db.sql_queries.insert import insert_into
from src.property.models import PropertyCreateInfo, PropertyInfo
from src.utils import list_dict_keys

property_router = APIRouter(prefix="/property", tags=["property"])
RETURNING_VALUE = "property_id"
PROPERTY_TABLE = 'property'


@property_router.post("/")
def create_property(
        property_info: Annotated[PropertyCreateInfo, Form()],
        conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]
):
    info = property_info.model_dump(exclude_unset=True, exclude_defaults=True)
    foreign_key = PropertyInfo.foreign_key(token_data.user_id)
    info.update(foreign_key)

    query = insert_into(PROPERTY_TABLE, list_dict_keys(info), returning=[RETURNING_VALUE])

    try:
        with conn_pool.connection() as conn:
            return conn.execute(query, info).fetchone()[0]
    except UniqueViolation as e:
        print(e)
        raise HTTPException(status_code=400, detail="User info already set")
    except ForeignKeyViolation as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"User {token_data.user_id} doesn't exist")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong")


@property_router.get("/test")
def test():
    return "test property"
