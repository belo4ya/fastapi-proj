import typing as t
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from app.core.db import SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin

__all__ = [
    'Employee',
    'Project',
    'EmployeeProjectLink',
]


class Employee(SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin, table=True):
    first_name: str
    last_name: str
    patronymic: str | None = None

    manager_id: int | None = Field(default=None, foreign_key="employee.id")

    manager: t.Optional['Employee'] = Relationship(
        back_populates="employees",
        sa_relationship_kwargs=dict(remote_side="Employee.id"),
    )
    employees: list['Employee'] = Relationship(back_populates="manager")

    projects: list['EmployeeProjectLink'] = Relationship(back_populates="employee")


class Project(SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin, table=True):
    tag: str
    name: str
    status: str
    start_date: datetime | None = None
    end_date: datetime | None = None

    resources: list['EmployeeProjectLink'] = Relationship(back_populates="project")


class EmployeeProjectLink(SQLModel, table=True):
    project_id: int | None = Field(default=None, primary_key=True, foreign_key="project.id")
    employee_id: int | None = Field(default=None, primary_key=True, foreign_key="employee.id")

    project: Project = Relationship(back_populates="resources")
    employee: Employee = Relationship(back_populates="projects")
