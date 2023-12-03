"""
Provides global settings for the application.

The config is loading the values for each parameter from the environment
(Environment Variables Values) using pydantic's `BaseSettings`.
"""

from pathlib import Path
from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """FRAAND Platform settings..."""

    class Config:
        """Extra configuration for the settings..."""

        case_sensitive = True

        env_file = '.env'
        env_file_encoding = 'utf-8'

    TITLE: str
    ENVIRONMENT: str

    # CORS Middleware
    CORS_ORIGINS: list[str]
    CORS_CREDENTIALS: bool
    CORS_METHODS: list[str]
    CORS_HEADERS: list[str]

    # Auth...
    AUTH_JWT_SECRET: str

    # PostgreSQL Database Connection
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URL: PostgresDsn | None

    @validator('SQLALCHEMY_DATABASE_URL', pre=True)
    def assemble_db_connection_string(cls, v: PostgresDsn | None, values: dict[str, Any]) -> str:
        """Composes `SQLALCHEMY_DATABASE_URL` parameter..."""

        if isinstance(v, str):
            return v

        # Error handling for missing values
        scheme = 'postgresql+asyncpg'
        user = values.get('POSTGRES_USER')
        password = values.get('POSTGRES_PASSWORD')
        host = values.get('POSTGRES_HOST')
        port = values.get('POSTGRES_PORT')
        path = values.get('POSTGRES_DB')

        if not all([user, password, host, port, path]):
            raise ValueError('DB')

        return PostgresDsn.build(
            scheme=scheme,
            user=values['POSTGRES_USER'],
            password=values['POSTGRES_PASSWORD'],
            host=values['POSTGRES_HOST'],
            port=values['POSTGRES_PORT'],
            path=f"/{values['POSTGRES_DB']}",
        )

    # Pagination
    PAGE_SIZE: int = 1000


if Path('.env'):
    settings = Settings('.env')  # type: ignore
else:
    raise FileNotFoundError('.env')
