from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from psycopg.rows import class_row

from src.auth.dependencies import AuthorizeUserDepends
from src.auth.models import TokenData
from src.db.pool_dependency import ConnectionPoolDepends
from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.insert import insert_into
from src.db.sql_queries.select_actions import select_from_table
from src.db.sql_queries.update_action import update_row
from src.db.sql_queries.utils import concat_sql_queries
from src.property.models import PropertyCreateInfo, PropertyInfo, PropertyUpdateInfo
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong")


@property_router.put("/{property_id}")
def create_new_user_info(
        property_id: int,
        property_info: Annotated[PropertyUpdateInfo, Form()], conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    info = property_info.model_dump(exclude_none=True)
    if not info:
        return HTTPException(status_code=400, detail=f"Cannot update property ({property_id}) with empty data")

    identify_property = PropertyInfo.foreign_key(token_data.user_id)
    identify_property.update({"property_id": property_id})

    query = update_row(
        list_dict_keys(info),
        list_dict_keys(identify_property),
        PROPERTY_TABLE,
        returning=[RETURNING_VALUE]
    )
    info.update(identify_property)

    try:
        with conn_pool.connection() as conn:
            return conn.execute(query, info).fetchone()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@property_router.get("/")
def get_user_properties(
        conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    identify_properties = PropertyInfo.foreign_key(token_data.user_id)
    query = concat_sql_queries(
        select_from_table(PROPERTY_TABLE),
        add_and_conditions(list_dict_keys(identify_properties))
    )
    try:
        with conn_pool.connection() as conn:
            conn.row_factory = class_row(PropertyInfo)
            result: PropertyInfo = conn.execute(query, identify_properties).fetchone()
            if not result:
                return None
            return result.model_dump(exclude_none=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@property_router.get("/{property_id}")
def get_user_property_by_id(
        property_id: int,
        conn_pool: ConnectionPoolDepends,
        token_data: Annotated[TokenData, AuthorizeUserDepends]):
    identify_properties = PropertyInfo.foreign_key(token_data.user_id)
    identify_properties.update({"property_id": property_id})
    query = concat_sql_queries(
        select_from_table(PROPERTY_TABLE),
        add_and_conditions(list_dict_keys(identify_properties))
    )
    try:
        with conn_pool.connection() as conn:
            conn.row_factory = class_row(PropertyInfo)
            result: PropertyInfo = conn.execute(query, identify_properties).fetchone()
            if not result:
                return None
            return result.model_dump(exclude_none=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@property_router.get("/test")
def test():
    return "test property"
