from fastapi.param_functions import Query

from app.schemas.constants import (
    PAGINATION_DEFAULT_PAGE,
    PAGINATION_DEFAULT_PAGE_SIZE
)


class PaginationParams:
    """Query parameters for pagination."""

    def __init__(
        self,
        page: int = Query(PAGINATION_DEFAULT_PAGE, gt=0),
        page_size: int = Query(PAGINATION_DEFAULT_PAGE_SIZE, gt=0)
    ) -> None:
        self.page = page
        self.page_size = page_size
