"""User-related dependencies..."""

import uuid

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase

from src.fraand_core.domains.users.manager import UserManager
from src.fraand_core.domains.users.models import User, get_user_db
from src.fraand_core.security.security import jwt_bearer_auth_backend


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) -> UserManager:
    """Returns the user manager of `SQLAlchemyUserDatabase`..."""

    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [jwt_bearer_auth_backend])
current_active_user = fastapi_users.current_user(active=True, optional=True)
