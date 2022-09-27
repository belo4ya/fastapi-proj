import typing as t

from fastapi import APIRouter, status
from fastapi import Depends

from app.api.v1.constants import Prefixes, Tags
from app.api.v1.dependencies import get_session
from app.api.v1.exceptions import raise_404 as _raise_404
from app.api.v1.projects import models
from app.api.v1.projects import schemas
from app.api.v1.services import CRUD
from app.core.db import SessionT

router = APIRouter(prefix=f"/{Prefixes.projects}", tags=[Tags.projects])


def raise_404(project_id: int) -> t.NoReturn:
    _raise_404(message=f"Project with id={project_id} not found")


def get_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Project]:
    return CRUD(session, models.Project)


@router.get("/{project_id}", response_model=schemas.ProjectRead)
async def get_project(
    project_id: int,
    crud: CRUD[models.Project] = Depends(get_crud),
):
    project = await crud.get_by_id(project_id)
    if not project:
        raise_404(project_id)

    return project


@router.get("", response_model=list[schemas.ProjectRead])
async def get_projects(
    crud: CRUD[models.Project] = Depends(get_crud),
):
    return await crud.get_all()


@router.post("", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: schemas.ProjectCreate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    project = models.Project.from_orm(data)
    async with session.begin():
        return await crud.save(project)


@router.patch("/{project_id}", response_model=schemas.ProjectRead)
async def update_project(
    project_id: int,
    data: schemas.ProjectUpdate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    async with session.begin():
        project = await crud.get_by_id(project_id)
        if not project:
            raise_404(project_id)

        for attr, value in data.dict(exclude_unset=True).items():
            setattr(project, attr, value)

        return await crud.save(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    async with session.begin():
        ok = await crud.delete_by_id(project_id)
    if not ok:
        raise_404(project_id)
