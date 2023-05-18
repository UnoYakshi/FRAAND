"""
The core application setup.

Includes:
- configuration
- middleware
- routers
- mounts
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.fraand_core.config import settings
from src.fraand_core.constants import STATIC_ABS_FILE_PATH, TEMPLATES_ABS_FILE_PATH
from src.fraand_core.db import init_db
from src.fraand_core.domains.users.dependencies import current_active_user
from src.fraand_core.domains.users.models import User
from src.fraand_core.routers import (
    auth_router,
    passwords_router,
    registration_router,
    users_router,
    verification_router,
)

SHOW_DOCS_ENVIRONMENT = ('dev', 'staging')

app_configs = {'title': settings.TITLE}
if settings.ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs['openapi_url'] = None  # Hide /docs...

app = FastAPI(**app_configs)

# Add middlewares, mounts, routers, etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.mount('/static', StaticFiles(directory=STATIC_ABS_FILE_PATH), name='static')
app_templates = Jinja2Templates(directory=TEMPLATES_ABS_FILE_PATH, auto_reload=True)

# Include auth-related routers...
app.include_router(auth_router, prefix='/auth/jwt', tags=['auth'])
app.include_router(registration_router, prefix='/auth', tags=['auth'])
app.include_router(passwords_router, prefix='/auth', tags=['auth'])
app.include_router(verification_router, prefix='/auth', tags=['auth'])
app.include_router(users_router, prefix='/users', tags=['users'])


@app.on_event('startup')
async def on_startup() -> None:
    """Before the start of the server..."""
    await init_db()


@app.get('/', response_class=HTMLResponse)
async def root(request: Request, user: Annotated[User | None, Depends(current_active_user)]) -> Response:
    """The home page of the platform."""
    rows = list(range(10))
    context = {
        'request': request,
        'rows': rows,
    }
    if user:
        context['current_user'] = user
    return app_templates.TemplateResponse(name='index.html', context=context)


@app.get('/authenticated-route')
async def authenticated_route(user: User = Depends(current_active_user)) -> dict[str, str]:
    """A simple check for an authenticated user..."""

    return {'message': f'Hello {user.email}!'}


@app.get('/ping')
async def ping() -> dict[str, str]:
    """Simple server pinging..."""

    return {'ping': 'pong!'}


@app.post('/search')
async def search(query: Annotated[str, Form()]) -> dict[str, str]:
    """Simple server pinging..."""

    return {'search_query': query}
