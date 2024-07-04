"""Dependencies for Deals domain..."""


from datetime import datetime, timedelta

from fastapi import Query


def deals_search_query(
    q: str | None = Query(default=None, min_length=2),
    due_date: datetime | None = Query(default=(datetime.now() + timedelta(days=14))),  # noqa: ARG001, B008
    skip: int = 0,
    limit: int = 100,
) -> dict[str, str | int]:
    """A shortcut to reduce the number of parameters for the /get_items endpoint..."""

    return {'q': q, 'skip': skip, 'limit': limit}
