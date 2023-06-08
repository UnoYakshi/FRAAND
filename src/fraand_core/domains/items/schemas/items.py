"""Pydantic schemas for Items..."""
import uuid

from pydantic.fields import Field
from pydantic.types import UUID4

from src.fraand_core.schemas import ORJSONModel


class ItemBaseSchema(ORJSONModel):
    """Base schema for Items..."""

    id: UUID4 | None  # noqa: A003

    name: str
    description: str | None

    # If the item should be browsable...
    is_published: bool = Field(default=True)

    # TODO: Make it some geo-data-based...
    city: str

    # Access granted to specific users or groups...
    # TODO: Add `access` field/relationship..

    owner_id: UUID4

    # TODO: Add `tags` field (one-to-many)...

    class Config:
        """Extra Item schema configuration..."""

        schema_extra = {
            'example': {
                'name': 'Very Cool Tool',
                'description': 'Tis but a nice thing to share amongst your kin!',
                'city': 'London',
                'owner_id': uuid.uuid4(),
            },
        }


class ItemCreateSchema(ItemBaseSchema):
    """Creation schema for Item..."""

    ...


class ItemUpdateSchema(ItemBaseSchema):
    """Update schema for Item..."""

    name: str | None
    description: str | None
    city: str | None
    owner_id: UUID4 | None


class ImageBaseSchema(ORJSONModel):
    """Base Image (for Items) schema..."""

    image: bytes

    item_uid: UUID4
    item: ItemBaseSchema
