"""Endpoints for users-related functionality..."""

from typing import Annotated

from fastapi import APIRouter, Depends

from src.fraand_core.schemas.user import User
from src.fraand_core.security import get_current_active_user

users_router = APIRouter(prefix='/users')


@users_router.get('/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    """Tries to retrieve the information about the current user, if logged-in..."""
    return current_user
