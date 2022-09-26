from fastapi import APIRouter

from app.api.v1 import projects

router = APIRouter(prefix="/v1", responses={404: {"description": "Not found"}})

router.include_router(projects.router)
