"""Schemas for users-related functionality..."""

import uuid

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate

from src.fraand_core.schemas import ORJSONModel


class BaseUserSchema(ORJSONModel, BaseUser[uuid.UUID]):
    """Regular platform user schema, can be used for Read operations..."""

    ...


class UserCreateSchema(ORJSONModel, BaseUserCreate):
    """User schema for Create operations..."""

    ...


class UserUpdateSchema(ORJSONModel, BaseUserUpdate):
    """User schema for Update operations..."""

    ...
