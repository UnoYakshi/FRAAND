"""ORM models for Items."""

import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.fraand_core.crud.base import BaseCRUD
from src.fraand_core.domains.items.schemas.items import ItemCreateSchema, ItemUpdateSchema
from src.fraand_core.models.base import Base, UUIDBase


class ItemTagAssoc(Base):
    """Association table for many-to-many relation between Items and Tags..."""

    __tablename__ = 'items_tags_at'

    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), primary_key=True)
    tag: Mapped['Tag'] = relationship(back_populates='items')

    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('items.id'), primary_key=True)
    item: Mapped['Item'] = relationship(back_populates='tags')


class Item(UUIDBase):
    """Items people can share with each other..."""

    __tablename__ = 'items'

    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    is_published: Mapped[bool | None] = mapped_column(default=True)
    city: Mapped[str | None] = mapped_column()

    tags: Mapped[set[ItemTagAssoc]] = relationship(back_populates='item')

    def get_contacts(self) -> dict[str, str]:
        """[WIP] Placeholder for retrieving contact information for this User's Item...."""
        return {'email': 'some_email@mail.inpls', 'Telegram': '@grociepo'}


class Image(UUIDBase):
    """Images files for items."""

    __tablename__ = 'images'

    image: Mapped[bytes] = mapped_column()

    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('items.id'))
    item: Mapped[Item] = relationship(Item, back_populates='images')


class Tag(Base):
    """Custom tags for Items made by Users upon Item creation/modification..."""

    __tablename__ = 'tags'

    id: Mapped[int] = Column(Integer, autoincrement=True, primary_key=True)  # noqa: A003
    name: Mapped[str] = Column(String, nullable=False)

    items: Mapped[set[ItemTagAssoc]] = relationship(back_populates='tag')


class ItemCRUD(BaseCRUD[Item, ItemCreateSchema, ItemUpdateSchema]):
    """Item CRUD manager..."""

    ...


item_crud_manager = ItemCRUD(Item)
