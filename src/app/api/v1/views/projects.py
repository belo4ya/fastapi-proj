from fastapi import APIRouter, Depends

from app.api.deps import get_projects_repo, get_session
from app.api.v1 import schemas
from app.core.db import SessionT
from app.domain import models
from app.domain import repositories as repos

router = APIRouter(prefix='/projects', tags=['projects'])


@router.get('', response_model=list[schemas.ProjectRead])
async def get_projects_view(
        repo: repos.ProjectsRepository = Depends(get_projects_repo)
):
    return await repo.get_all()


@router.post('', response_model=schemas.ProjectRead)
async def create_project_view(
        data: schemas.ProjectCreate,
        session: SessionT = Depends(get_session),
        repo: repos.ProjectsRepository = Depends(get_projects_repo)
):
    project = models.Project.from_orm(data)
    async with session.begin():
        return await repo.save(project)
