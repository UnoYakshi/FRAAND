"""TypeVars for CRUD-manager..."""

from typing import TypeVar

from pydantic import BaseModel

from src.fraand_core.models import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
