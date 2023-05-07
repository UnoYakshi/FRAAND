"""Endpoints for users-related functionality..."""

from src.fraand_core.domains.users.routes import (  # noqa: F401
    auth_router,
    passwords_router,
    registration_router,
    users_router,
    verification_router,
)
