from pydantic import BaseModel
from typing import TypeVar, Generic, Sequence

TListItem = TypeVar("TListItem")


class PaginationResponse(BaseModel):
    offset: int
    limit: int
    total: int


class ListPaginationResponse(BaseModel, Generic[TListItem]):
    items: Sequence[TListItem]
    pagination: PaginationResponse
