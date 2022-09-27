from fastapi import Query
from pydantic import BaseModel

from app.core.db import async_session_factory, SessionT


async def get_session() -> SessionT:
    async with async_session_factory() as session:
        yield session


class PaginationQuery(BaseModel):
    offset: int | None = None
    limit: int | None = None


def pagination_query(offset: int | None = Query(None), limit: int | None = Query(None)) -> PaginationQuery:
    return PaginationQuery(offset=offset, limit=limit)
