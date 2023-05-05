"""ORM models for Items."""

from sqlalchemy import Boolean, Column, ForeignKey, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.fraand_core.crud.base import BaseCRUD
from src.fraand_core.domains.items.schemas.items import ItemCreateSchema, ItemUpdateSchema
from src.fraand_core.models import UUIDBase


class Item(UUIDBase):
    """Items people can share with each other..."""

    __tablename__ = 'items'

    name: str = Column(String)
    description: str = Column(String)
    is_published: bool = Column(Boolean, default=True)
    city: str = Column(String)

    def get_contacts(self) -> dict[str, str]:
        """[WIP] Placeholder for retrieving contact information for this User's Item...."""
        return {'email': 'some_email@mail.inpls', 'Telegram': '@grociepo'}


class Image(UUIDBase):
    """Images files for items."""

    __tablename__ = 'images'

    image = Column(LargeBinary, nullable=False)

    item_uid = Column(UUID, ForeignKey('items.uid'))
    item = relationship(Item, back_populates='images')


class ItemCRUD(BaseCRUD[Item, ItemCreateSchema, ItemUpdateSchema]):
    """Item CRUD manager..."""

    ...


item_crud_manager = ItemCRUD(Item)
