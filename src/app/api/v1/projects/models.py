import typing as t
from datetime import datetime

from sqlmodel import Relationship

from app.core.db import SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin

if t.TYPE_CHECKING:
    from app.api.v1.models import EmployeeProjectLink


class Project(SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin, table=True):
    tag: str
    name: str
    status: str
    start_date: datetime | None = None
    end_date: datetime | None = None

    resources: list["EmployeeProjectLink"] = Relationship(back_populates="project")
