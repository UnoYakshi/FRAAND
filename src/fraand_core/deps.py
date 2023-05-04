"""General platform dependencies..."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.fraand_core.db import AsyncSessionFactory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yields asynchronous database session, closes the session at the end..."""

    async_session: AsyncSession = AsyncSessionFactory()  # type: ignore
    try:
        yield async_session
    finally:
        await async_session.close()
