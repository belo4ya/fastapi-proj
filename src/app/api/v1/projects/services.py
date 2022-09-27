from sqlalchemy import sql

from app.api.v1.employees.models import Employee
from app.core.db import SessionT


async def get_resources_by_ids(session: SessionT, ids: list[int]) -> list[Employee]:
    stmt = sql.select(Employee).where(Employee.id.in_(ids))  # type: ignore
    return (await session.scalars(stmt)).all()
