"""User ORM module (via FasstAPI-Users)..."""

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.fraand_core.deps import get_async_session
from src.fraand_core.models.base import Base


class User(Base, SQLAlchemyBaseUserTableUUID):
    """Base model for Users..."""

    ...


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> SQLAlchemyUserDatabase:
    """Returns the User database from the database via FastAPI-Users adapter..."""
    yield SQLAlchemyUserDatabase(session, User)
