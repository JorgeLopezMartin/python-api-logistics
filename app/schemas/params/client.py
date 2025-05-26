from dataclasses import dataclass
from typing import Optional
from fastapi import Depends, Query

from app.schemas.params.pagination.pagination import PaginationParams


@dataclass
class ClientFilters:
    """Query parameters for filtering clients"""

    name: Optional[str] = Query(None)


class ClientParams:
    """Query parameters for listing clients"""

    def __init__(
        self,
        filters: ClientFilters = Depends(),
        pagination: PaginationParams = Depends()
    ) -> None:
        self.filters = filters
        self.pagination = pagination