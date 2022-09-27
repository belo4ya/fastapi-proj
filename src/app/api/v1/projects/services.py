from sqlalchemy import sql

from app.api.v1.projects import models
from app.api.v1.services import CRUD
from app.core.db import SessionT


def get_crud(session: SessionT) -> CRUD[models.Project]:
    return CRUD(session, models.Project)


async def get_projects_by_ids(session: SessionT, ids: list[int]) -> list[models.Project]:
    stmt = sql.select(models.Project).where(models.Project.id.in_(ids))  # type: ignore
    return (await session.scalars(stmt)).all()
