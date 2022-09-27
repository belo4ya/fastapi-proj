import typing as t
from enum import Enum

from sqlmodel import Relationship, Field

from app.core.db import SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin

if t.TYPE_CHECKING:
    pass


class UserRoles(str, Enum):
    # users
    employee = "employee"
    manager = "manager"
    project_owner = "project_owner"
    project_manager = "project_manager"
    hr_manger = "hr_manger"
    tech_support = "tech_support"

    # service
    admin = "admin"


class User(SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin, table=True):
    jwt_sub: str = Field(unique=True)
    role: UserRoles
