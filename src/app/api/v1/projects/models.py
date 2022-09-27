import typing as t
from datetime import datetime

from sqlmodel import Relationship

from app.api.v1.constants import ProjectStatuses
from app.api.v1.models import ProjectResourceLink
from app.core.db import SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin

if t.TYPE_CHECKING:
    from app.api.v1.employees.models import Employee

__all__ = [
    "Project",
]


class Project(SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin, table=True):
    tag: str
    title: str
    status: ProjectStatuses = ProjectStatuses.active
    start_date: datetime | None = None
    end_date: datetime | None = None

    resources: list["Employee"] = Relationship(
        back_populates="projects",
        link_model=ProjectResourceLink,
        # lazy="selectin" нужно для корректной работы:
        # project.resources = ...
        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#synopsis-orm
        # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#relationship-loading-techniques
        # альтернатива - sql.select(Project).options(orm.selectinload(Project.resources))
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
