import typing as t

from sqlalchemy import sql

from app.core.db import SessionT, SurrogateKeyMixin, SoftDeleteMixin

_M = t.TypeVar("_M", bound=t.Union[SurrogateKeyMixin, SoftDeleteMixin])


class CRUD(t.Generic[_M]):
    def __init__(self, session: SessionT, model_cls: t.Type[_M]):
        self.session = session
        self.model_cls = model_cls

    async def save(self, entity: _M) -> _M:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def save_all(self, entities: list[_M]) -> list[_M]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get_by_id(self, id_: int, with_deleted: bool = False) -> _M | None:
        exec_opts = {"with_deleted": with_deleted}
        stmt = sql.select(self.model_cls).where(self.model_cls.id == id_)
        return await self.session.scalar(stmt, execution_options=exec_opts)

    async def get_all(self, with_deleted: bool = False) -> list[_M]:
        exec_opts = {"with_deleted": with_deleted}
        stmt = sql.select(self.model_cls)
        return (await self.session.scalars(stmt, execution_options=exec_opts)).all()

    async def delete(self, entity: _M, soft: bool = True) -> None:
        if soft:
            entity.deleted = True
            await self.save(entity)
        else:
            await self.session.delete(entity)

    async def delete_by_id(self, id_: int, soft: bool = True) -> bool:
        if soft:
            stmt = sql.update(self.model_cls).values(deleted=True)
        else:
            stmt = sql.delete(self.model_cls)

        stmt = stmt.where(self.model_cls.id == id_)
        res = await self.session.execute(stmt)
        return res.rowcount > 0
