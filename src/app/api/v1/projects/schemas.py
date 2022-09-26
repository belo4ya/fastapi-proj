from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    tag: str
    name: str
    status: str = "active"
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
