"""
The core application setup.

Includes:
- configuration
- middleware
- routers
- mounts
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from src.fraand_core.config import settings
from src.fraand_core.constants import STATIC_ABS_FILE_PATH
from src.fraand_core.db import init_db
from src.fraand_core.domains.users.dependencies import current_active_user
from src.fraand_core.domains.users.models import User
from src.fraand_core.routers import include_routers
from src.fraand_core.templates import app_templates

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

include_routers(app)


@app.on_event('startup')
async def on_startup() -> None:
    """Before the start of the server..."""
    await init_db()


@app.get('/', response_class=HTMLResponse)
async def root(request: Request, user: Annotated[User | None, Depends(current_active_user)]) -> Response:
    """The home page of the platform..."""

    context = {
        'request': request,
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
