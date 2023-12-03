"""
Endpoints for search domain.

/search
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from src.fraand_core.domains.users.dependencies import current_active_user
from src.fraand_core.domains.users.models import User
from src.fraand_core.templates import app_templates

search_router = APIRouter()


@search_router.get('/search/', response_class=HTMLResponse)
async def get_search_results(query: str, user: Annotated[User | None, Depends(current_active_user)]) -> HTMLResponse:
    """Return search result for the user query."""
    items = [
        {
            'id': '05ee38de-76c2-4751-bb34-d579237c5a9e',
            'name': 'Very Cool Tool',
            'description': 'Tis but a nice thing to share amongst your kin!',
            'city': 'London',
            'owner_id': '25321f69-3162-47ae-8aa9-5fa5f559beaa',
        },
    ]

    context = {'query': query, 'items': items}
    if user:
        context['current_user'] = user
    return app_templates.TemplateResponse('widgets/search/results.html', context=context)
