"""
Proxy endpoints for HTML Forms...

The proxies exist for:
- registration
- login
- WIP: logout
"""


from typing import Annotated

import httpx
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

fastapi_users_proxy_router = APIRouter()


@fastapi_users_proxy_router.post('/login')
async def login_proxy(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> RedirectResponse:
    """WIP: HTML Form based solution to pass credentials to /auth/jwt/login..."""
    async with httpx.AsyncClient() as client:
        login_response = await client.post(
            url=f'{request.base_url}auth/jwt/login',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={'username': email, 'password': password},
        )

    # Also add an Auth Token we received to the redirect...
    redirect_response = RedirectResponse(url=f'{request.base_url}', status_code=status.HTTP_302_FOUND)
    redirect_response.set_cookie(key='auth', value=login_response.cookies.get('auth'), httponly=True)

    return redirect_response


@fastapi_users_proxy_router.post('/logout')
async def logout_proxy(request: Request) -> RedirectResponse:
    """WIP: HTML Form based solution to pass credentials to /auth/jwt/logout..."""

    async with httpx.AsyncClient() as client:

        await client.post(
            url=f'{request.base_url}auth/jwt/logout',
            headers={
                'accept': 'application/json',
            },
            cookies={'auth': request.cookies.get('auth')},
        )

    redirect_response = RedirectResponse(url=f'{request.base_url}', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie('auth')

    return redirect_response


@fastapi_users_proxy_router.post('/register')
async def register_proxy(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> RedirectResponse:
    """WIP: HTML Form based solution to pass credentials to /auth/register..."""

    async with httpx.AsyncClient() as client:
        await client.post(url=f'{request.base_url}auth/register', json={'email': email, 'password': password})

    # HTTP_302_FOUND can be used, too...
    return RedirectResponse(url=f'{request.base_url}', status_code=status.HTTP_303_SEE_OTHER)
