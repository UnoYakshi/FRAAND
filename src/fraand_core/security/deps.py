"""Dependencies for security-related functionality..."""

from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.fraand_core.schemas.user import User
from src.fraand_core.security.security import decode_token, oauth2_scheme


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Tries to retrieve the user by the given token..."""

    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """The same as `get_current_user()` with additional check for `User.disabled`..."""

    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')

    return current_user
