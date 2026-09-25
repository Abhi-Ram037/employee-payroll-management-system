from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    total: int
    pages: int
    data: list[T]