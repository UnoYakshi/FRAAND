"""
Items routers...

- CRUD router is responsible for DB interaction
- Pages router is for HTML-pages generation
"""


from fastapi import APIRouter

from .crud import items_crud_router
from .pages import items_pages_router

items_router = APIRouter(prefix='/items', tags=['items'])

items_router.include_router(items_pages_router)
items_router.include_router(items_crud_router)
