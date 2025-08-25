import os

from pydantic_settings import BaseSettings

is_dev = os.getenv("type") == "dev"
env_file = "../.env.dev" if is_dev else ""


class Settings(BaseSettings):
    # Admin Credentials
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str

    # Postgres
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: str

    # OAuth2
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float


settings = Settings(_env_file=env_file)
