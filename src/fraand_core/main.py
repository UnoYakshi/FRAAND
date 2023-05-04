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
from fastapi.templating import Jinja2Templates

from src.fraand_core.config import settings
from src.fraand_core.constants import STATIC_ABS_FILE_PATH, TEMPLATES_ABS_FILE_PATH
from src.fraand_core.db import init_db
from src.fraand_core.routers import security_router, users_router
from src.fraand_core.security import oauth2_scheme

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
app_templates = Jinja2Templates(directory=TEMPLATES_ABS_FILE_PATH)

app.include_router(security_router)
app.include_router(users_router)


@app.on_event('startup')
async def on_startup() -> None:
    """Before the start of the server..."""
    await init_db()


@app.get('/', response_class=HTMLResponse)
async def root(request: Request) -> Response:
    """The home page of the platform."""
    rows = list(range(10))
    return app_templates.TemplateResponse(name='index.html', context={'request': request, 'rows': rows})


@app.get('/auth-ping')
async def auth_ping(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
    """Simple server pinging with authorization..."""
    return {'ping': 'pong!', 'token': token}


@app.get('/ping')
async def ping() -> dict[str, str]:
    """Simple server pinging."""
    return {'ping': 'pong!'}
