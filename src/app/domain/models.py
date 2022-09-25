from datetime import datetime

from sqlmodel import SQLModel, Field

__all__ = [
    'Project',
]


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tag: str
    name: str
    start_date: datetime | None = None
    end_date: datetime | None = None
