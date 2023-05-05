"""Defines base class with shared attributes for models (database tables)."""

import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import MetaData, SQLModel

POSTGRES_INDEXES_NAMING_CONVENTION = {
    'ix': '%(column_0_label)s_idx',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': '%(table_name)s_%(constraint_name)s_check',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

Base = declarative_base(metadata=metadata)
SQLModel.metadata = Base.metadata


class UUIDBase(Base):
    """Base class with UUID."""

    __abstract__ = True

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
