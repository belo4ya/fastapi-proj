from sqlmodel import SQLModel, Field

__all__ = [
    "ProjectResourceLink",
]


class ProjectResourceLink(SQLModel, table=True):
    project_id: int | None = Field(default=None, foreign_key="project.id", primary_key=True)
    resource_id: int | None = Field(default=None, foreign_key="employee.id", primary_key=True)
