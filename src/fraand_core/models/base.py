"""
Defines base class with shared attributes for models (database tables).
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import orjson
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, root_validator
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

Base = declarative_base()
Base.metadata = metadata
SQLModel.metadata = Base.metadata


def orjson_dumps(v, *, default):
    """`orjson.dumps()` returns bytes, to match standard `json.dumps()` we need to decode..."""
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo('UTC'))

    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}  # method for customer JSON encoding of datetime fields

    @root_validator()
    def set_null_microseconds(cls, data: dict) -> dict:
        """Drops microseconds in all the datetime field values."""
        datetime_fields = {k: v.replace(microsecond=0) for k, v in data.items() if isinstance(k, datetime)}

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs):
        """Returns a dict which contains only serializable fields."""
        default_dict = super().dict(**kwargs)

        return jsonable_encoder(default_dict)
