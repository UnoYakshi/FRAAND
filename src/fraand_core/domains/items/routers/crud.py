"""
CRUD-router for Items domain...

Endpoints are:
- GET /{id}
- GET /? q= & skip= & limit= & should_search_in_name= & should_search_in_description=
- POST /create
- PUT /update/{id}
- DELETE /delete/{id]
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select

from src.fraand_core.crud.base import BaseCRUD
from src.fraand_core.deps import AsyncSession, get_async_session
from src.fraand_core.domains.items.dependencies import search_query
from src.fraand_core.domains.items.models import Item
from src.fraand_core.domains.items.schemas.items import ItemBaseSchema, ItemCreateSchema, ItemUpdateSchema


class ItemCRUD(BaseCRUD[Item, ItemCreateSchema, ItemUpdateSchema]):
    """Item CRUD manager..."""

    ...


items_crud_router = APIRouter(prefix='/crud', tags=['items', 'crud'])
item_crud_manager = ItemCRUD(Item)


@items_crud_router.get(
    path='/{item_id:str}',
    response_model=ItemBaseSchema,
    responses={
        status.HTTP_200_OK: {'description': 'The item is found.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'No item with such [UU]ID is found.'},
    },
)
async def get_item(item_id: Annotated[UUID, ...], session: AsyncSession = Depends(get_async_session)) -> ItemBaseSchema:
    """Returns an Item by its [UU]ID..."""

    item: Item = await item_crud_manager.read(session, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'No Item[UUID={item_id}] found...',
        )

    return ItemBaseSchema.from_orm(item)


@items_crud_router.get(
    path='/',
    response_model=list[ItemBaseSchema],
    responses={
        status.HTTP_200_OK: {'description': 'Item with the given data is successfully created.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'If item is not found by the given UUID.'},
    },
)
async def get_items(
    search_params: Annotated[dict, Depends(search_query)],
    should_search_in_name: bool = True,
    should_search_in_description: bool = True,
    belongs_to_users: list[UUID] | None = None,
    session: AsyncSession = Depends(get_async_session),
) -> list[ItemBaseSchema]:
    """
    Returns Items by the given query...

    :parameter search_params:
            :query: Will be used to find somewhat matching [to the value] results;
                      both name and description will be used; as OR predicates...
            :skip: How many Items to skip in the results...
            :limit: How many Items to include...
    """

    q = search_params.get('q')
    skip = search_params['skip']
    limit = search_params['limit']

    # Compose the select-query...
    query = select(Item)

    # Add filters for name and/or description if needed...
    if q:
        if should_search_in_name and should_search_in_description:
            query = query.where(
                or_(
                    Item.name.ilike(q),
                    Item.name.icontains(q),
                    Item.description.ilike(q),
                    Item.description.icontains(q),
                ),
            )
        elif should_search_in_name:
            query = query.where(or_(Item.name.ilike(q), Item.name.icontains(q)))
        elif should_search_in_description:
            query = query.where(or_(Item.description.ilike(q), Item.description.icontains(q)))

    if belongs_to_users:
        query = query.where(Item.owner_id.in_(belongs_to_users))

    # Add pagination...
    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    items = result.scalars().all()
    return [ItemBaseSchema.from_orm(item) for item in items]


@items_crud_router.post(
    path='/create',
    response_model=ItemBaseSchema,
    responses={
        status.HTTP_201_CREATED: {'description': 'A new item is created.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Incorrect data provided for the new item.'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_item(data: ItemCreateSchema, session: AsyncSession = Depends(get_async_session)) -> ItemBaseSchema:
    """Create a new Item with the provided data..."""

    try:
        item = await item_crud_manager.create(session, data)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Incorrect data [{data}]: {error}',
        ) from error

    return ItemBaseSchema.from_orm(item)


@items_crud_router.post(
    path='/update/{item_id:str}',
    response_model=ItemBaseSchema,
    responses={
        status.HTTP_200_OK: {
            'description': 'Item (provided by UUID) is updated with the given data. POST-version for HTTP/1.x',
        },
        status.HTTP_400_BAD_REQUEST: {'description': 'If item is not found by the given UUID.'},
    },
)
@items_crud_router.put(
    path='/update/{item_id:str}',
    response_model=ItemBaseSchema,
    responses={
        status.HTTP_200_OK: {'description': 'Item (provided by UUID) is updated with the given data.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'If item is not found by the given UUID.'},
    },
)
async def update_item(
    item_id: UUID,
    data: ItemUpdateSchema,
    session: AsyncSession = Depends(get_async_session),
) -> ItemBaseSchema:
    """Updates the Item (by its ID) with the given `data`..."""

    item = await item_crud_manager.read(session, id=item_id)
    updated_item = await item_crud_manager.update(session, item, data)
    return ItemBaseSchema.from_orm(updated_item)


@items_crud_router.delete(
    path='/delete/{item_id:str}',
    response_model=ItemBaseSchema,
    responses={
        status.HTTP_200_OK: {'description': 'Item is removed.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'If item is not found by the given UUID.'},
    },
)
async def delete_item(item_id: UUID, session: AsyncSession = Depends(get_async_session)) -> ItemBaseSchema:
    """Removes the item by its ID (if exists)..."""

    item = await item_crud_manager.read(session, id=item_id)
    await item_crud_manager.delete(session, item)
    return ItemBaseSchema.from_orm(item)
