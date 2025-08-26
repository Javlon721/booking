from typing import TypeAlias, Annotated

from fastapi import Depends
from psycopg_pool import ConnectionPool

from src.db.connection import connection_manager

ConnectionPoolDepends: TypeAlias = Annotated[ConnectionPool, Depends(connection_manager.get_connection_pool)]
