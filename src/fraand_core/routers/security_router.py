"""Endpoints for security-related functionality..."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.fraand_core.schemas.user import UserInDB
from src.fraand_core.security import fake_users_db, hash_password

security_router = APIRouter()


@security_router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    """Logs the user with the given form data..."""

    user_data = fake_users_db.get(form_data.username)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect credentials (username)')

    user = UserInDB(**user_data)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect credentials (password)')

    return {'access_token': user.username, 'token_type': 'bearer'}
