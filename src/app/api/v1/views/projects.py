from datetime import datetime

from fastapi import APIRouter

from app.api.v1 import schemas

router = APIRouter(prefix='/projects', tags=['projects'])

projects = [
    schemas.ProjectOut(
        id=0,
        tag='ABC',
        name='Проект #1'
    ),
    schemas.ProjectOut(
        id=1,
        tag='QWE',
        name='Проект #2',
        start_date=datetime(2022, 9, 25)
    ),
    schemas.ProjectOut(
        id=2,
        tag='ZXC',
        name='Проект #3',
        start_date=datetime(2022, 9, 25),
        end_date=datetime(2024, 9, 25)),
]


@router.get('', response_model=list[schemas.ProjectOut])
async def get_projects_view():
    return projects
