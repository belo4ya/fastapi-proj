from sqlalchemy import sql

from app.api.v1.employees.models import Employee
from app.api.v1.projects import models
from app.api.v1.services import CRUD
from app.core.db import SessionT


def get_crud(session: SessionT) -> CRUD[models.Project]:
    return CRUD(session, models.Project)


async def get_resources_by_ids(session: SessionT, ids: list[int]) -> list[Employee]:
    stmt = sql.select(Employee).where(Employee.id.in_(ids))  # type: ignore
    return (await session.scalars(stmt)).all()
