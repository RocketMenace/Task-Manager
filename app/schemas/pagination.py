from pydantic import BaseModel


class PaginationResponse(BaseModel):
    offset: int
    limit: int
    total: int


class ListPaginationResponse(BaseModel):
    items: list
    pagination: PaginationResponse
