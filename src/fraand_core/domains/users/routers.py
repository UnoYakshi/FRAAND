"""All the users/authentication/authorization routers..."""

from src.fraand_core.domains.users.dependencies import fastapi_users
from src.fraand_core.domains.users.schemas import BaseUserSchema, UserCreateSchema, UserUpdateSchema
from src.fraand_core.security.security import jwt_cookie_auth_backend

# TODO: Change verification to `True`!..
auth_router = fastapi_users.get_auth_router(jwt_cookie_auth_backend, requires_verification=False)
registration_router = fastapi_users.get_register_router(BaseUserSchema, UserCreateSchema)
verification_router = fastapi_users.get_verify_router(BaseUserSchema)
passwords_router = fastapi_users.get_reset_password_router()
# TODO: Change verification to `True`!..
users_router = fastapi_users.get_users_router(BaseUserSchema, UserUpdateSchema, requires_verification=False)
