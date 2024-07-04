"""
Schemas for Deals...

Includes:
- status
- CRUD
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic.main import BaseModel


class DealStatus(str, Enum):
    """
    Deal's status...

    INIT = just initiated, no actions have been performed yet
    PENDING = waiting for confirmation from all or some of the parties
    BORROWED = deal is confirmed, Item is in use
    FAILED = failed for any reason
    """

    INIT = 'INIT'
    PENDING = 'PENDING'
    BORROWED = 'BORROWED'
    FAILED = 'FAILED'


class DealBaseSchema(BaseModel):
    """Base for CRUD..."""

    item_id: UUID
    status: DealStatus
    created_at: datetime | None
    due_date: datetime | None


class DealCreateSchema(DealBaseSchema):
    """Creation schema for Deals..."""

    uuid: UUID


class DealUpdateSchema(DealBaseSchema):
    """Update schema for Deals..."""

    ...
