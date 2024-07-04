"""
Items routers...

- CRUD router is responsible for DB interaction
- Pages router is for HTML-pages generation
"""


from fastapi import APIRouter

from .crud import deals_crud_router
from .rent import rent_router

deals_router = APIRouter(prefix='/deals', tags=['deals'])

deals_router.include_router(rent_router)
deals_router.include_router(deals_crud_router)
