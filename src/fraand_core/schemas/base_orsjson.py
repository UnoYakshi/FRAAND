"""Custom base class for Pydantic schemes..."""

from datetime import datetime
from typing import Any, Callable
from zoneinfo import ZoneInfo

import orjson
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Extra, root_validator


def orjson_dumps(v: Any, *, default: Callable[[Any], Any]) -> str:  # noqa: ANN401
    """Internal function for ORJSONModel to work instead `json.dumps()`..."""
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    """Encodes datetime fields, ensuring forced time zone is used..."""
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo('UTC'))

    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


class ORJSONModel(BaseModel):
    """Faster (because of ORJSON) "alternative" for Pydantic BaseModel..."""

    class Config:
        """ORJSONModel functions overriding..."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}  # method for customer JSON encoding of datetime fields

        extra = Extra.forbid

    @root_validator()
    def set_null_microseconds(cls, data: dict) -> dict:
        """Drops microseconds in all the datetime field values."""
        datetime_fields = {k: v.replace(microsecond=0) for k, v in data.items() if isinstance(k, datetime)}

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs) -> dict:  # noqa: ANN003
        """Returns a dict which contains only serializable fields."""
        default_dict = super().dict(**kwargs)

        return jsonable_encoder(default_dict)
