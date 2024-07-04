"""
Endpoints for search domain.

/search
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.fraand_core.deps import get_async_session
from src.fraand_core.domains.items.dependencies import search_query
from src.fraand_core.domains.items.routers.crud import get_items
from src.fraand_core.domains.users.dependencies import current_active_user
from src.fraand_core.domains.users.models import User
from src.fraand_core.templates import app_templates

search_router = APIRouter(prefix='/search', tags=['search'])


@search_router.get('/', response_class=HTMLResponse)
async def get_search_results(
    search_params: Annotated[dict, Depends(search_query)],
    request: Request,
    user: Annotated[User | None, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Return Items search result for the user query..."""

    items = await get_items(
        search_params=search_params,
        should_search_in_name=True,
        session=session,
    )

    context = {
        'request': request,
        'q': search_params['q'],
        'skip': search_params.get('skip'),
        'limit': search_params.get('limit'),
        'items': items,
    }
    if user:
        context['current_user'] = user

    return app_templates.TemplateResponse('widgets/search/results.html', context=context)
