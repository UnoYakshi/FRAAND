"""
CRUD-router for Items domain...

Endpoints are:
- GET /{id}
- GET /?skip=&limit=
- POST /create
- PUT /update/{id}
- DELETE /delete/{id]
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.fraand_core.crud.base import BaseCRUD
from src.fraand_core.deps import AsyncSession, get_async_session
from src.fraand_core.domains.items.models import Item
from src.fraand_core.domains.items.schemas.items import ItemBaseSchema, ItemCreateSchema, ItemUpdateSchema

items_router = APIRouter(prefix='/items', tags=['items'])


class ItemCRUD(BaseCRUD[Item, ItemCreateSchema, ItemUpdateSchema]):
    """Item CRUD manager..."""

    ...


item_crud_manager = ItemCRUD(Item)


@items_router.get(
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


@items_router.get(
    path='/',
    response_model=list[ItemBaseSchema],
    responses={
        status.HTTP_200_OK: {'description': 'Item with the given data is successfully created.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'If item is not found by the given UUID.'},
    },
)
async def get_items(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
) -> list[ItemBaseSchema]:
    """..."""

    items = await item_crud_manager.read_many(session, skip=skip, limit=limit)
    return [ItemBaseSchema.from_orm(item) for item in items]


@items_router.post(
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


@items_router.put(
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


@items_router.delete(
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
