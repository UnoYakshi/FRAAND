"""Schemas for users-related functionality..."""

from src.fraand_core.schemas import ORJSONModel


class User(ORJSONModel):
    """Regular platform user schema..."""

    username: str
    email: str | None = None  # Can be used to reset credentials?..
    disabled: bool = False


class UserInDB(User):
    """User represented in the database, i.e., no sensitive data is saved in a raw, non-hashed and unsalted format..."""

    hashed_password: bytes
