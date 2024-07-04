"""Renting process models..."""

import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.fraand_core.domains.deals.schemas import DealStatus
from src.fraand_core.models.base import Base, UUIDBase


class Deal(UUIDBase):
    """
    Represents an item renting process entity...

    Supports multiple users (via UserDealAssoc table) finishing certain steps towards the Deal agreement...
    """

    if TYPE_CHECKING:
        from src.fraand_core.domains.items.models import Item
        from src.fraand_core.domains.users.models import User

    __tablename__ = 'deals'

    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('items.id'))
    item: Mapped['Item'] = relationship(back_populates='deals')

    status: Mapped[DealStatus] = mapped_column(ENUM(DealStatus, name='deal_status', create_type=True))

    users: Mapped[list['User']] = relationship(secondary='users_deals_at')

    created_at: Mapped[datetime.datetime | None] = mapped_column(default=None)
    due_date: Mapped[datetime.datetime | None] = mapped_column(default=None)


class UserDealAssoc(Base):
    """
    Many-to-many relationship between User and Deal tables...

    Also, has a bunch of extra boolean flags for renting process...
    """

    __tablename__ = 'users_deals_at'

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), primary_key=True)

    deal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('deals.id'), primary_key=True)

    # Intermediate flags for renting process...
    agreed_on_terms: Mapped[bool] = mapped_column(default=False)
    confirmed_borrowing: Mapped[bool] = mapped_column(default=False)
    confirmed_return: Mapped[bool] = mapped_column(default=False)
