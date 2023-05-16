"""Pydantic schemas for Items..."""

from pydantic.fields import Field
from pydantic.types import UUID4

from src.fraand_core.schemas import ORJSONModel


class ItemBaseSchema(ORJSONModel):
    """Base schema for Items..."""

    name: str
    description: str | None

    # If the item should be browsable...
    published: bool = Field(default=True)

    # TODO: Make it some geo-data-based...
    city: str

    # Access granted to specific users or groups...
    # TODO: Add `access` field/relationship..

    owner_id: UUID4

    # TODO: Add `tags` field (one-to-many)...


class ItemCreateSchema(ItemBaseSchema):
    """Creation schema for Item..."""

    ...


class ItemUpdateSchema(ItemCreateSchema):
    """Update schema for Item..."""

    ...


class ImageBaseSchema(ORJSONModel):
    """Base Image (for Items) schema..."""

    image: bytes

    item_uid: UUID4
    item: ItemBaseSchema
