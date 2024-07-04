"""Routers aggregator..."""

from fastapi import FastAPI

from .deals_router import deals_router
from .items_router import items_router
from .search_router import search_router
from .security_router import fastapi_users_proxy_router
from .users_router import auth_router, passwords_router, registration_router, users_router, verification_router


def include_routers(app: FastAPI) -> None:
    """
    Includes all the routers in the given FastAPI application...

    Somewhat helps to fix circular imports and leads towards better code organization...
    """

    # Include auth-related routers...
    app.include_router(auth_router, prefix='/auth/jwt', tags=['auth'])
    app.include_router(registration_router, prefix='/auth', tags=['auth'])
    app.include_router(passwords_router, prefix='/auth', tags=['auth'])
    app.include_router(verification_router, prefix='/auth', tags=['auth'])
    app.include_router(users_router, prefix='/users', tags=['users'])

    # Include proxy login/logout/register router...
    app.include_router(fastapi_users_proxy_router, prefix='/proxy', tags=['auth', 'user'])

    # Include search router...
    app.include_router(search_router)

    # Include Items-related routers...
    app.include_router(items_router)

    app.include_router(deals_router)
