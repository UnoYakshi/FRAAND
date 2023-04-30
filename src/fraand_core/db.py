"""
Sets up postgres connection pool.
"""

# TODO: Should it be async_session_maker?..
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.fraand_core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, future=True, echo=False)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
