from datetime import datetime

from pydantic import BaseModel, constr


class ProjectOut(BaseModel):
    id: int
    tag: constr(to_upper=True)
    name: str
    start_date: datetime | None = None
    end_date: datetime | None = None
