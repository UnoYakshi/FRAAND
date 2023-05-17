"""User-related dependencies..."""


import uuid

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

import src.fraand_core.domains.users.models as user_models
from src.fraand_core.deps import get_async_session
from src.fraand_core.domains.users.manager import UserManager
from src.fraand_core.security.security import jwt_bearer_auth_backend, jwt_cookie_auth_backend


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> SQLAlchemyUserDatabase:
    """Returns the User database from the database via FastAPI-Users adapter..."""

    yield SQLAlchemyUserDatabase(session, user_models.User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) -> UserManager:
    """Returns the user manager of `SQLAlchemyUserDatabase`..."""

    yield UserManager(user_db)


fastapi_users = FastAPIUsers[user_models.User, uuid.UUID](
    get_user_manager,
    [jwt_cookie_auth_backend, jwt_bearer_auth_backend],
)
current_active_user = fastapi_users.current_user(active=True, optional=True)
