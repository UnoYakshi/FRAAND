from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.fraand_core.config import settings
from src.fraand_core.db import init_db

SHOW_DOCS_ENVIRONMENT = ('dev', 'staging')

app_configs = {'title': settings.TITLE}
if settings.ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs['openapi_url'] = None  # Hide /docs...

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


@app.on_event('startup')
async def on_startup():
    await init_db()


@app.get('/')
async def root() -> str:
    return 'Howdy!'


@app.get('/ping')
async def ping() -> dict[str, str]:
    return {'ping': 'pong!'}
