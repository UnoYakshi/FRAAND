"""CRUD router for Deals..."""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from src.fraand_core.crud.base import BaseCRUD
from src.fraand_core.deps import AsyncSession, get_async_session
from src.fraand_core.domains.deals.dependencies import deals_search_query
from src.fraand_core.domains.deals.models import Deal
from src.fraand_core.domains.deals.schemas import DealBaseSchema, DealCreateSchema, DealUpdateSchema
from src.fraand_core.domains.items.models import Item


class DealCRUD(BaseCRUD[Deal, DealCreateSchema, DealUpdateSchema]):
    """Deal CRUD manager..."""

    ...


deals_crud_router = APIRouter(prefix='/crud', tags=['deals', 'crud'])
deal_crud_manager = DealCRUD(Deal)
logger = logging.getLogger(__name__)


@deals_crud_router.get(
    path='/{deal_id:str}',
    response_model=DealBaseSchema,
    responses={
        status.HTTP_200_OK: {'description': 'The deal is found.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'No deal with such [UU]ID is found.'},
    },
)
async def get_deal(deal_id: Annotated[UUID, ...], session: AsyncSession = Depends(get_async_session)) -> DealBaseSchema:
    """Returns a Deal by its [UU]ID..."""

    deal: Deal = await deal_crud_manager.read(session, id=deal_id)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'No Deal[UUID={deal_id}] found...',
        )

    return DealBaseSchema.from_orm(deal)


@deals_crud_router.get(
    path='/',
    response_model=list[DealBaseSchema],
    responses={
        status.HTTP_200_OK: {'description': 'Deal with the given data is successfully created.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'If deal is not found by the given UUID.'},
    },
)
async def get_deals(
    search_params: Annotated[dict, Depends(deals_search_query)],
    session: AsyncSession = Depends(get_async_session),
) -> list[DealBaseSchema]:
    """
    Returns Deals by the given query...

    :parameter search_params:
            :query: Will be used to find somewhat matching [to the value] results;
                      both name and description will be used; as OR predicates...
            :skip: How many Deals to skip in the results...
            :limit: How many Deals to include...
    """

    q = search_params.get('q')
    skip = search_params['skip']
    limit = search_params['limit']
    logger.info(f'Deals: q={q}, skip={skip}, limit={limit}')

    # Compose the select-query...
    query = select(Deal).join(Item, Item.id == Deal.item_id)  # It was Name.c.field...

    # Add filters for name and/or description if needed...

    # Add pagination...
    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    deals = result.scalars().all()
    return [DealBaseSchema.from_orm(deal) for deal in deals]


@deals_crud_router.post(
    path='/create',
    response_model=DealBaseSchema,
    responses={
        status.HTTP_201_CREATED: {'description': 'A new deal is created.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Incorrect data provided for the new deal.'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_deal(data: DealCreateSchema, session: AsyncSession = Depends(get_async_session)) -> DealBaseSchema:
    """Create a new Deal with the provided data..."""

    try:
        deal = await deal_crud_manager.create(session, data)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Incorrect data [{data}]: {error}',
        ) from error

    return DealBaseSchema.from_orm(deal)


@deals_crud_router.post(
    path='/update/{deal_id:str}',
    response_model=DealBaseSchema,
    responses={
        status.HTTP_200_OK: {
            'description': 'Deal (provided by UUID) is updated with the given data. POST-version for HTTP/1.x',
        },
        status.HTTP_400_BAD_REQUEST: {'description': 'If deal is not found by the given UUID.'},
    },
)
@deals_crud_router.put(
    path='/update/{deal_id:str}',
    response_model=DealBaseSchema,
    responses={
        status.HTTP_200_OK: {'description': 'Deal (provided by UUID) is updated with the given data.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'If deal is not found by the given UUID.'},
    },
)
async def update_deal(
    deal_id: UUID,
    data: DealUpdateSchema,
    session: AsyncSession = Depends(get_async_session),
) -> DealBaseSchema:
    """Updates the Deal (by its ID) with the given `data`..."""

    deal = await deal_crud_manager.read(session, id=deal_id)
    updated_deal = await deal_crud_manager.update(session, deal, data)
    return DealBaseSchema.from_orm(updated_deal)


@deals_crud_router.delete(
    path='/delete/{deal_id:str}',
    response_model=DealBaseSchema,
    responses={
        status.HTTP_200_OK: {'description': 'Deal is removed.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'If deal is not found by the given UUID.'},
    },
)
async def delete_deal(deal_id: UUID, session: AsyncSession = Depends(get_async_session)) -> DealBaseSchema:
    """Removes the deal by its ID (if exists)..."""

    deal = await deal_crud_manager.read(session, id=deal_id)
    await deal_crud_manager.delete(session, deal)
    return DealBaseSchema.from_orm(deal)
