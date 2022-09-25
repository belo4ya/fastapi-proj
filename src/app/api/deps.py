from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session as _get_session


async def get_session() -> AsyncSession:
    return _get_session()
