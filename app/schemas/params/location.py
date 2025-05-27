from dataclasses import dataclass
from typing import Optional
from fastapi import Depends, Query

from app.schemas.params.pagination.pagination import PaginationParams


@dataclass
class LocationFilters:
    """Query parameters for filtering locations"""

    name: Optional[str] = Query(None)


class LocationParams:
    """Query parameters for listing locations"""

    def __init__ (
        self,
        filters: LocationFilters = Depends(),
        pagination: PaginationParams = Depends()
    ) -> None:
        self.filters = filters
        self.pagination = pagination
