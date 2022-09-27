from sqlalchemy import sql

from app.api.v1.employees import models
from app.api.v1.services import CRUD
from app.core.db import SessionT


def get_crud(session: SessionT) -> CRUD[models.Employee]:
    return CRUD(session, models.Employee)


async def get_employees_by_ids(session: SessionT, ids: list[int]) -> list[models.Employee]:
    stmt = sql.select(models.Employee).where(models.Employee.id.in_(ids))  # type: ignore
    return (await session.scalars(stmt)).all()
