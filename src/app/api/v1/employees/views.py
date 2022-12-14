import typing as t

from fastapi import APIRouter, status
from fastapi import Depends
from pydantic import parse_obj_as

from app.api.v1.constants import Prefixes, Tags
from app.api.v1.dependencies import get_session, PaginationQuery, pagination_query
from app.api.v1.employees import models
from app.api.v1.employees import schemas
from app.api.v1.employees import services
from app.api.v1.exceptions import raise_404 as _raise_404
from app.api.v1.projects.services import get_projects_by_ids
from app.api.v1.services import CRUD
from app.core.db import SessionT

router = APIRouter(prefix=f"/{Prefixes.employees}", tags=[Tags.employees])


def raise_404(employee_id: int) -> t.NoReturn:
    _raise_404(message=f"Employee with id={employee_id} not found")


def get_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Employee]:
    return services.get_crud(session)


@router.get("/{employee_id}", response_model=schemas.EmployeeRead)
async def get_employee(
    employee_id: int,
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    employee = await crud.get_by_id(employee_id)
    if not employee:
        raise_404(employee_id)
    return employee


@router.get("", response_model=schemas.EmployeePagination)
async def get_employees(
    page_q: PaginationQuery = Depends(pagination_query),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    employees, total = await crud.get_all_paginate(offset=page_q.offset, limit=page_q.limit)
    return schemas.EmployeePagination(
        offset=page_q.offset,
        limit=page_q.limit,
        total=total,
        results=parse_obj_as(list[schemas.EmployeeRead], employees),
    )


@router.post("", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee(
    data: schemas.EmployeeCreate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    async with session.begin():
        new_data = data.dict()
        if data.employees:
            employees_ids = [employee.id for employee in data.employees]
            new_data["employees"] = await services.get_employees_by_ids(session, employees_ids)

        employee = models.Employee(**new_data)
        return await crud.save(employee)


@router.patch("/{employee_id}", response_model=schemas.EmployeeRead)
async def update_employee(
    employee_id: int,
    data: schemas.EmployeeUpdate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    async with session.begin():
        employee = await crud.get_by_id(employee_id)
        if not employee:
            raise_404(employee_id)

        update_data = data.dict(exclude_unset=True)
        if "employees" in update_data:
            employees_ids = [employee.id for employee in data.employees]
            update_data["employees"] = await services.get_employees_by_ids(session, employees_ids)
        if "projects" in update_data:
            projects_ids = [project.id for project in data.projects]
            update_data["projects"] = await get_projects_by_ids(session, projects_ids)

        for attr, value in update_data.items():
            setattr(employee, attr, value)

        return await crud.save(employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    async with session.begin():
        ok = await crud.delete_by_id(employee_id)
    if not ok:
        raise_404(employee_id)
