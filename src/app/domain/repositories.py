from sqlalchemy import sql

from app.core.db import SessionT
from app.domain import models


class ProjectsRepository:

    def __init__(self, session: SessionT):
        self.session = session

    async def save(self, entity: models.Project) -> models.Project:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get_by_id(self, id_: int, with_deleted: bool = False) -> models.Project:
        exec_opts = {'with_deleted': with_deleted}
        stmt = sql.select(models.Project).where(models.Project.id == id_).execution_options(**exec_opts)
        return await self.session.exec(stmt).scalar_one()

    async def get_all(self, with_deleted: bool = False) -> list[models.Project]:
        exec_opts = {'with_deleted': with_deleted}
        stmt = sql.select(models.Project).execution_options(**exec_opts)
        return (await self.session.scalars(stmt)).all()

    async def delete_by_id(self, id_: int, soft=True) -> bool:
        if soft:
            stmt = sql.update(models.Project).values(deleted=True)
        else:
            stmt = sql.delete(models.Project)

        stmt = stmt.where(models.Project.id == id_)
        res = await self.session.exec(stmt)
        return res.rowcount > 0
