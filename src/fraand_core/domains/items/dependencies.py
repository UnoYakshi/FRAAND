"""Put your FastAPI dependencies for Items domain here..."""

from fastapi import Query


def search_query(
    q: str | None = Query(default=None, min_length=2),
    skip: int = 0,
    limit: int = 100,
) -> dict[str, str | int]:
    """A shortcut to reduce the number of parameters for the /get_items endpoint..."""

    return {'q': q, 'skip': skip, 'limit': limit}
