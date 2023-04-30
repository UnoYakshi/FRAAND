"""
Sets up postgres connection pool.
"""

# TODO: Should it be async_session_maker?..
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.fraand_core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, future=True, echo=False)

async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
