from datetime import datetime

from pydantic import BaseModel

from app.api.v1.constants import ProjectStatuses
from app.api.v1.schemas import PaginationSchema


class ProjectResourceID(BaseModel):
    id: int


class ProjectResourceRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None = None


class ProjectBase(BaseModel):
    tag: str
    title: str
    status: ProjectStatuses
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectCreate(ProjectBase):
    status: ProjectStatuses = ProjectStatuses.active
    resources: list[ProjectResourceID] = []


class ProjectUpdate(ProjectBase):
    tag: str | None = None
    title: str | None = None
    status: ProjectStatuses | None = None
    resources: list[ProjectResourceID] = []


class ProjectRead(ProjectBase):
    id: int
    resources: list[ProjectResourceRead] = []


class ProjectPagination(PaginationSchema[ProjectRead]):
    pass
