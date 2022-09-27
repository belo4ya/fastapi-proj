import typing as t

from pydantic import BaseModel
from pydantic.generics import GenericModel

_T = t.TypeVar("_T", bound=BaseModel)


class PaginationSchema(GenericModel, t.Generic[_T]):
    offset: int | None
    limit: int | None
    total: int
    results: list[_T]
