"""
CRUD processes for Items...

GET: generates HTML-pages for Items-related functionality...
POST+: performs logic with the database for Items (from CRUD-router)...
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.fraand_core.constants import TEMPLATES_ABS_FILE_PATH
from src.fraand_core.deps import get_async_session
from src.fraand_core.domains.items.dependencies import search_query
from src.fraand_core.domains.items.routers.crud import create_item as create_item_crud
from src.fraand_core.domains.items.routers.crud import delete_item as delete_item_crud
from src.fraand_core.domains.items.routers.crud import get_item as get_item_crud
from src.fraand_core.domains.items.routers.crud import get_items as get_items_crud
from src.fraand_core.domains.items.routers.crud import update_item as update_item_crud
from src.fraand_core.domains.items.schemas.items import ItemBaseSchema, ItemCreateSchema, ItemUpdateSchema
from src.fraand_core.domains.users.dependencies import current_active_user
from src.fraand_core.domains.users.models import User

app_templates = Jinja2Templates(directory=TEMPLATES_ABS_FILE_PATH, auto_reload=True)

items_pages_router = APIRouter(prefix='/pages', tags=['items', 'html'])


@items_pages_router.get(
    path='/get',
    description='Generates the Item List form...',
    status_code=status.HTTP_200_OK,
)
async def get_user_items(
    search_params: Annotated[dict, Depends(search_query)],
    request: Request,
    user: Annotated[User | None, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """Generates current User's Items HTML-page..."""

    context = {
        'request': request,
        'current_user': user,
    }

    items = await get_items_crud(
        search_params=search_params,
        belongs_to_users=[user.id],
        session=session,
    )
    if items:
        context['items'] = [ItemBaseSchema.from_orm(item) for item in items]

    return app_templates.TemplateResponse(name='widgets/items/items_list.html', context=context)


@items_pages_router.get(path='/add', description='Generates the Item creation form...', status_code=status.HTTP_200_OK)
@items_pages_router.post(
    path='/add',
    description='Actually creates the item in the DB, will also show its card...',
    status_code=status.HTTP_201_CREATED,
)
async def add_item(
    request: Request,
    user: Annotated[User | None, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """
    Item Create process...

    - GET: returns Item creation HTML page...
    - POST: uses CRUD manager to actually create a new item with the provided data...
    """

    context = {'request': request, 'current_user': user}

    if request.method == 'POST':
        async with request.form() as form:
            # Add the new item to the DB according to the data...
            response = await create_item_crud(
                data=ItemCreateSchema(
                    name=form['name'],
                    description=form['description'],
                    city=form['city'],
                    owner_id=form['owner_id'],
                ),
                session=session,
            )
            context['item'] = response

    return app_templates.TemplateResponse(name='widgets/items/crud/add.html', context=context)


@items_pages_router.get(
    path='/get/{item_id}',
    description='Generates HTML-page for the given Item (by its UUID)...',
    status_code=status.HTTP_200_OK,
)
async def get_item(
    item_id: UUID,
    request: Request,
    user: Annotated[User | None, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """Generates Read/display HTML-page for the given Item UUID..."""

    context = {
        'request': request,
    }

    if user:
        context['current_user'] = user

    item = await get_item_crud(item_id=item_id, session=session)
    if item:
        context['item'] = ItemBaseSchema.from_orm(item)

    return app_templates.TemplateResponse(name='widgets/items/crud/detail.html', context=context)


@items_pages_router.get(
    path='/edit/{item_id}',
    description='Generates Update HTML-page...',
    status_code=status.HTTP_200_OK,
)
@items_pages_router.post(
    path='/edit/{item_id}',
    description='[HTTP/1.1] Actually updates the Item, retrieves data from the form...',
    status_code=status.HTTP_200_OK,
)
@items_pages_router.put(
    path='/edit/{item_id}',
    description='[HTTP/2.0] Actually updates the Item, retrieves data from the form...',
    status_code=status.HTTP_200_OK,
)
async def edit_item(
    item_id: UUID,
    request: Request,
    user: Annotated[User | None, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """
    Item Update process...

    GET: Generates Edit HTML-page for the given Item UUID...
    POST, PUT: Actually changes the Item's fields in the database...
    """

    context = {
        'request': request,
    }

    if user:
        context['current_user'] = user

    if request.method == 'GET':
        item = await get_item_crud(item_id=item_id, session=session)
        if item:
            context['item'] = ItemBaseSchema.from_orm(item)

    if request.method in ('POST', 'PUT'):
        async with request.form() as form:
            # Add the new item to the DB according to the data...
            response = await update_item_crud(
                item_id=item_id,
                data=ItemUpdateSchema(
                    name=form['name'],
                    description=form['description'],
                    city=form['city'],
                ),
                session=session,
            )
            context['item'] = response

    return app_templates.TemplateResponse(name='widgets/items/crud/edit.html', context=context)


@items_pages_router.get(
    path='/delete/{item_id}',
    description='Generates the Item deletion confirmation form...',
    status_code=status.HTTP_200_OK,
)
@items_pages_router.post(
    path='/delete/{item_id}',
    description='[HTTP/1.1] Actually deletes the item from the DB...',
    status_code=status.HTTP_204_NO_CONTENT,
)
@items_pages_router.delete(
    path='/delete/{item_id}',
    description='[HTTP/2.0] Actually deletes the item from the DB...',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(
    item_id: UUID,
    request: Request,
    user: Annotated[User | None, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """
    Full Item deletion process, including HTML-page and logic...

    GET: Generates delete confirmation HTML page for the given Item UUID...
    POST, DELETE: Actually deletes the Item by its UUID...
    """

    context = {
        'request': request,
    }
    if user:
        context['current_user'] = user

    if request.method == 'GET':
        item = await get_item_crud(item_id=item_id, session=session)
        if not item:
            context['item_id'] = item_id
            return app_templates.TemplateResponse(name='widgets/items/404_item.html', context=context)

        context['item'] = ItemBaseSchema.from_orm(item)

        return app_templates.TemplateResponse(name='widgets/items/crud/confirm_delete.html', context=context)

    if request.method in ('DELETE', 'POST'):
        response = await delete_item_crud(
            item_id=item_id,
            session=session,
        )
        context['item'] = response
        return app_templates.TemplateResponse(name='widgets/items/crud/detail.html', context=context)

    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
