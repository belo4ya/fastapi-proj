from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, ORMExecuteState, Session, with_loader_criteria
from sqlmodel import SQLModel, Field

from app.settings import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
    future=True,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

SessionT = AsyncSession | Session


async def get_session() -> SessionT:
    async with async_session() as session:
        yield session


class SurrogateKeyMixin(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class TimestampMixin(SQLModel):
    created_at: datetime | None = Field(
        sa_column=sa.Column(
            sa.DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )

    updated_at: datetime | None = Field(
        sa_column=sa.Column(
            sa.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )
    )


class _SoftDeleteMixin:
    __config__ = None
    deleted = sa.Column('deleted', sa.Boolean, default=False, nullable=False)


class SoftDeleteMixin(SQLModel, _SoftDeleteMixin):
    pass


@sa.event.listens_for(Session, 'do_orm_execute')
def _add_filtering_criteria(execute_state: ORMExecuteState):
    if (
            not execute_state.is_column_load
            and not execute_state.is_relationship_load
            and not execute_state.execution_options.get('with_deleted', False)
    ):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                _SoftDeleteMixin,
                lambda cls: cls.deleted == sa.false(),
                include_aliases=True,
            )
        )
