"""User ORM module (via FasstAPI-Users)..."""

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

import src.fraand_core.models.base as base_models


class User(SQLAlchemyBaseUserTableUUID, base_models.Base):
    """Base model for Users..."""

    __tablename__ = 'users'

    items: Mapped[list['Item']] = relationship(back_populates='owner')  # noqa: F821
