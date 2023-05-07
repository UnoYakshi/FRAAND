"""..."""

import uuid

from fastapi_users import FastAPIUsers

from src.fraand_core.domains.users.dependencies import get_user_manager
from src.fraand_core.domains.users.models import User
from src.fraand_core.domains.users.schemas import BaseUserSchema, UserCreateSchema, UserUpdateSchema
from src.fraand_core.security.security import jwt_bearer_auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [jwt_bearer_auth_backend])
current_active_user = fastapi_users.current_user(active=True)

# TODO: Change verification to `True`!..
auth_router = fastapi_users.get_auth_router(jwt_bearer_auth_backend, requires_verification=False)
registration_router = fastapi_users.get_register_router(BaseUserSchema, UserCreateSchema)
verification_router = fastapi_users.get_verify_router(BaseUserSchema)
passwords_router = fastapi_users.get_reset_password_router()
# TODO: Change verification to `True`!..
users_router = fastapi_users.get_users_router(BaseUserSchema, UserUpdateSchema, requires_verification=False)
