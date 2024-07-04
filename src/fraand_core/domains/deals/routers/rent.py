"""
WIP renting process...

Reference: docs/flow.md
"""
import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.fraand_core.deps import get_async_session
from src.fraand_core.domains.deals.routers.crud import deal_crud_manager
from src.fraand_core.domains.deals.schemas import DealCreateSchema, DealStatus

rent_router = APIRouter(prefix='/rent', tags=['deals'])
logger = logging.getLogger(__name__)


@rent_router.post(
    path='/initiate/',
    status_code=status.HTTP_201_CREATED,
)
async def initiate_deal(item_id: UUID, borrower_id: UUID, session: AsyncSession = Depends(get_async_session)) -> None:
    """WIP Initiation Process..."""

    new_deal = DealCreateSchema(
        item_id=item_id,
        borrower_id=borrower_id,
        status=DealStatus.INIT,
    )
    deal_crud_manager.create(
        session=session,
        in_obj=...,
    )
    logger.info(f'{new_deal}: {item_id}, {borrower_id}')


@rent_router.post('/{deal_id}/confirm_reservation/')
async def confirm_reservation(deal_id: UUID, lender_id: UUID) -> None:
    """WIP Reservation/Booking Confirmation..."""

    logger.info(f'Deal [{deal_id}]: confirm reservation for Lender [{lender_id}].')


@rent_router.post('/{deal_id}/confirm_borrowed/')
async def confirm_borrowed(deal_id: UUID, due_date: Optional[str] = Body(None)) -> None:
    """WIP Confirm the Item is borrowed..."""

    logger.info(f'Deal [{deal_id}]: confirm borrowing due to {due_date}...')


@rent_router.post('/{deal_id}/fail_deal/')
async def fail_deal(deal_id: UUID) -> None:
    """WIP Fail the Deal..."""

    logger.info(f'Deal [{deal_id}]: fail.')
