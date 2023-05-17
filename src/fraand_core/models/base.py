"""Defines base class with shared attributes for models (database tables)."""

import uuid

from sqlalchemy import Column, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase

POSTGRES_INDEXES_NAMING_CONVENTION = {
    'ix': '%(column_0_label)s_idx',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': '%(table_name)s_%(constraint_name)s_check',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}
base_metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(DeclarativeBase):
    """The base declarative class for all models..."""

    # TODO: Should we use it?.. ``__allow_unmapped__ = True``

    metadata = base_metadata


class UUIDBase(Base):
    """Base class with UUID."""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # noqa: A003
