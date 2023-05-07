"""User-related dependencies..."""

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from src.fraand_core.domains.users.manager import UserManager
from src.fraand_core.domains.users.models import get_user_db


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) -> UserManager:
    """Returns the user manager of `SQLAlchemyUserDatabase`..."""

    yield UserManager(user_db)
