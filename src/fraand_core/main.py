from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.fraand_core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


@app.get('/')
async def root() -> str:
    return 'Howdy!'


@app.get('/ping')
async def ping() -> dict[str, str]:
    return {'ping': 'pong!'}
