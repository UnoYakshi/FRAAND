"""Tags-related Pydantic schemas..."""

from src.fraand_core.schemas import ORJSONModel


class ItemTagBaseSchema(ORJSONModel):
    """Base schema for Tags (for Items)..."""

    name: str
