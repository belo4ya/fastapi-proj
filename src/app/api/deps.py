from functools import lru_cache

from fastapi import Depends

from app.core.db import get_session as _get_session, SessionT
from app.domain import repositories as repos

get_session = _get_session  # TODO: как из тебя достать объект session?


@lru_cache
def get_projects_repo(session: SessionT = Depends(get_session)) -> repos.ProjectsRepository:
    return repos.ProjectsRepository(session)
