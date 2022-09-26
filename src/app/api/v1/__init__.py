from fastapi import APIRouter

from .views import projects

router = APIRouter(prefix="/v1")
router.include_router(projects.router)
