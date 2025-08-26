from psycopg_pool import ConnectionPool

from src.config import DB_CONFIG


class DBConnectionManager:
    old_pool: ConnectionPool | None = None

    def __init__(self):
        if not DBConnectionManager.old_pool:
            pool = ConnectionPool(
                f"dbname={DB_CONFIG.dbname} user={DB_CONFIG.user} password={DB_CONFIG.password} host={DB_CONFIG.host} port={DB_CONFIG.port}",
                max_size=DB_CONFIG.connection_pool_max_size,
            )
            DBConnectionManager.old_pool = pool
        self.connection_pool: ConnectionPool = DBConnectionManager.old_pool

    def get_connection_pool(self) -> ConnectionPool:
        return self.connection_pool

    def close_connection_pool(self):
        self.connection_pool.close()


connection_manager = DBConnectionManager()
