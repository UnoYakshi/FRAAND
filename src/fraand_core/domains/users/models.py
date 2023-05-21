"""User ORM module (via FasstAPI-Users)..."""

from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

import src.fraand_core.models.base as base_models


class User(SQLAlchemyBaseUserTableUUID, base_models.Base):
    """Base model for Users..."""

    __tablename__ = 'users'

    if TYPE_CHECKING:
        from src.fraand_core.domains.items.models import Item

    items: Mapped[list['Item']] = relationship(back_populates='owner')
