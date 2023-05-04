"""
Provides global settings for the application.

The config is loading the values for each parameter from the environment
(Environment Variables Values) using pydantic's `BaseSettings`.
"""

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
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values['POSTGRES_USER'],
            password=values['POSTGRES_PASSWORD'],
            host=values['POSTGRES_HOST'],
            port=values['POSTGRES_PORT'],
            path=f"/{values['POSTGRES_DB']}",
        )

    # Pagination
    PAGE_SIZE: int = 1000


settings = Settings('.env')  # type: ignore
