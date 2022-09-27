import typing as t

from sqlmodel import Relationship, Field

from app.core.db import SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin

if t.TYPE_CHECKING:
    from app.api.v1.models import EmployeeProjectLink


class Employee(SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin, table=True):
    first_name: str
    last_name: str
    patronymic: str | None = None

    manager_id: int | None = Field(default=None, foreign_key="employee.id")
    manager: t.Optional["Employee"] = Relationship(
        back_populates="employees",
        sa_relationship_kwargs=dict(remote_side="Employee.id"),
    )
    employees: list["Employee"] = Relationship(back_populates="manager")

    projects: list["EmployeeProjectLink"] = Relationship(back_populates="employee")
