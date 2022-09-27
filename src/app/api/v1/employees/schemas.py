from datetime import datetime

from pydantic import BaseModel

from app.api.v1.constants import ProjectStatuses
from app.api.v1.schemas import PaginationSchema


class EmployeeNestedID(BaseModel):
    id: int


class EmployeeNestedRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None = None


class EmployeeProjectID(BaseModel):
    id: int


class EmployeeProjectRead(BaseModel):
    id: int
    tag: str
    title: str
    status: ProjectStatuses
    start_date: datetime | None = None
    end_date: datetime | None = None


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None = None


class EmployeeCreate(EmployeeBase):
    manager_id: int | None = None
    employees: list[EmployeeNestedID] = []


class EmployeeUpdate(EmployeeBase):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None

    manager_id: int | None = None
    employees: list[EmployeeNestedID] = []
    projects: list[EmployeeProjectID] = []


class EmployeeRead(EmployeeBase):
    id: int
    manager_id: int | None = None
    employees: list[EmployeeNestedRead] = []
    projects: list[EmployeeProjectRead] = []


class EmployeePagination(PaginationSchema[EmployeeRead]):
    pass
