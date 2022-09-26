import typing as t

from fastapi import HTTPException, status


def raise_404(message: str) -> t.NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=[{"msg": message}],
    )
