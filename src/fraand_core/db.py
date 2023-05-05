"""Sets up PostgreSQL connection pool..."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.fraand_core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, future=True, echo=True)

AsyncSessionFactory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """Logs the database connection info [after migrations, before the server]..."""

    async with engine.begin() as conn:
        logging.info(conn.info)
