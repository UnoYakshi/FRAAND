"""
User manager module is responsible for all the user-related utility functionality...

It includes:
- registration callbacks
- passwords-related functionality callbacks and password validation
- verification callbacks
- users CRUD callbacks


Reference: https://fastapi-users.github.io/fastapi-users/11.0/configuration/user-manager/
"""

import logging
import re
import uuid
from typing import Any, Union

from fastapi import Request, Response
from fastapi_users import BaseUserManager, InvalidPasswordException, UUIDIDMixin

from src.fraand_core.config import settings
from src.fraand_core.domains.users.models import User
from src.fraand_core.domains.users.schemas import UserCreateSchema

logger = logging.getLogger('fastapi')


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """All the UUID-based User management logic..."""

    reset_password_token_secret = settings.AUTH_JWT_SECRET
    verification_token_secret = settings.AUTH_JWT_SECRET

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        """Perform logic after successful user registration."""

        logger.info(f'User [{user.id}] has registered.')
        logger.debug(f'Request: {request}.')

    async def on_after_update(self, user: User, update_dict: dict[str, Any], request: Request | None = None) -> None:
        """Perform logic after successful user update."""

        logger.info(f'User [{user.id}] has been updated with: {update_dict}.')
        logger.debug(f'Request: {request}.')

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        """
        Perform logic after user login.

        :param user: The user that is logging in.
        :param request: FastAPI request.
        :param response: Response built by the transport.
        """

        logger.info(f'User [{user.id}] logged in.')
        logger.debug(f'Request: {request.headers}.')
        logger.debug(f'Response: {response}.')

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None) -> None:
        """
        Perform logic after successful forgot password request.

        WIP: Sends an e-mail with the link (and the token) that allows the user to reset their password...
        """

        logger.info(f'User [{user.id}] has forgot their password. Reset token: {token}')
        logger.debug(f'Request: {request}.')

    async def on_after_reset_password(self, user: User, request: Request | None = None) -> None:
        """
        Perform logic after successful password reset.

        WIP: Sends an e-mail to the concerned user to warn about the password has been changed...
        (and that they should take action if they think they have been hacked)
        """

        logger.info(f'User [{user.id}] has reset their password.')
        logger.debug(f'Request: {request}.')

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None) -> None:
        """
        Perform logic after successful verification request.

        WIP: Sends an e-mail with the link (and the token) that allows the user to verify their e-mail...
        """

        logger.info(f'Verification requested for user [{user.id}]. Verification token: {token}')
        logger.debug(f'Request: {request}.')

    async def on_after_verify(self, user: User, request: Request | None = None) -> None:
        """Perform logic after successful user verification."""

        logger.info(f'User {user.id} has been verified')
        logger.debug(f'Request: {request}.')

    async def on_before_delete(self, user: User, request: Request | None = None) -> None:
        """Perform logic before user delete."""

        logger.info(f'User [{user.id}] is going to be deleted...')
        logger.debug(f'Request: {request}.')

    async def on_after_delete(self, user: User, request: Request | None = None) -> None:
        """Perform logic before user delete."""

        logger.info(f'User [{user.id}] is successfully deleted.')
        logger.debug(f'Request: {request}.')

    async def validate_password(self, password: str, user: Union[UserCreateSchema, User]) -> None:
        """
        Password validation...

        :raises InvalidPasswordException: if password is:
                                            - too small,
                                            - doesn't include digits, capital and small letters,
                                            - contains e-mail...
        """

        min_chars = 12

        if len(password) < min_chars:
            raise InvalidPasswordException(reason=f'Password should be at least {min_chars} characters.')

        if re.search('[0-9]', password) is None:
            raise InvalidPasswordException(reason='Password should include digits.')

        if user.email in password:
            raise InvalidPasswordException(reason='Password should not contain e-mail.')

        if re.search('[A-Z]', password) is None:
            raise InvalidPasswordException(reason='Password should include a capital letter.')

        if re.search('[a-z]', password) is None:
            raise InvalidPasswordException(reason='Password should include a lower-case letter.')
