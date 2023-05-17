"""User ORM module (via FasstAPI-Users)..."""

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

import src.fraand_core.models.base as base_models


class User(SQLAlchemyBaseUserTableUUID, base_models.Base):
    """Base model for Users..."""

    __tablename__ = 'users'
