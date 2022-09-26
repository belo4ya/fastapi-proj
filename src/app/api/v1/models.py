import typing as t

from sqlmodel import SQLModel, Field, Relationship

if t.TYPE_CHECKING:
    from app.api.v1.projects.models import Project
    from app.api.v1.employees.models import Employee


class EmployeeProjectLink(SQLModel, table=True):
    project_id: int | None = Field(default=None, primary_key=True, foreign_key="project.id")
    employee_id: int | None = Field(default=None, primary_key=True, foreign_key="employee.id")

    project: "Project" = Relationship(back_populates="resources")
    employee: "Employee" = Relationship(back_populates="projects")
