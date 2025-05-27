# pylint: disable=too-many-ancestors,abstract-method
from dataclasses import dataclass
from typing import Generic, List, Type, TypeVar

from sqlalchemy.orm import Query, Session

from app.models.base import BaseModel

ItemT = TypeVar('ItemT')


class Page(Generic[ItemT]):
    """Paginated response from repository."""

    @dataclass
    class Pagination:
        page: int
        page_size: int
        total: int

    data: List[ItemT]
    pagination: Pagination

    def __init__(
            self,
            data: List[ItemT],
            page: int,
            page_size: int,
            total: int
    ) -> None:
        self.data = data
        self.pagination = self.Pagination(page, page_size, total)


class PaginatedQuery(Query):
    """Queries with filter and pagination support."""

    def __init__(self, session: Session, entity: Type[BaseModel]) -> None:
        super().__init__(entity, session=session)
        self.entity = entity

    def paginate(self, page: int, page_size: int) -> Page:
        offset = page_size * (page - 1)
        order_by = self.entity.id

        items = self.order_by(order_by).limit(page_size).offset(offset).all()
        total = self.count()

        return Page(items, page, page_size, total)
