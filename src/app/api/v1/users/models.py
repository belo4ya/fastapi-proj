from sqlmodel import Field

from app.api.v1.constants import UserRoles
from app.core.db import SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin

__all__ = [
    "User",
]


class User(SurrogateKeyMixin, SoftDeleteMixin, TimestampMixin, table=True):
    sso_user_id: str = Field(unique=True)
    role: UserRoles
