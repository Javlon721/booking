import os
from dataclasses import dataclass

from pydantic_settings import BaseSettings

is_dev = os.getenv("type") == "dev"
env_file = "../.env.dev" if is_dev else ""


@dataclass
class DBConfig:
    dbname: str
    user: str
    password: str
    host: str
    port: str
    connection_pool_max_size: int


class _Settings(BaseSettings):
    # Admin Credentials
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str

    # Postgres
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: str
    CONNECTION_POOL_MAX_SIZE: int

    # OAuth2
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float

    def db_config(self) -> DBConfig:
        return DBConfig(
            dbname=self.POSTGRES_DB,
            user=self.DB_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            connection_pool_max_size=self.CONNECTION_POOL_MAX_SIZE,
        )


SETTINGS = _Settings(_env_file=env_file)
DB_CONFIG = SETTINGS.db_config()
