from dataclasses import dataclass
from typing import Optional
from fastapi import Depends, Query

from app.schemas.params.pagination.pagination import PaginationParams


@dataclass
class VesselFilters:
    """Query parameters for filtering vessels"""

    name: Optional[str] = Query(None)
    capacity: Optional[str] = Query(None)


class VesselParams:
    """Query parameters for listing vessels"""

    def __init__(
        self,
        filters: VesselFilters = Depends(),
        pagination: PaginationParams = Depends()
    ) -> None:
        self.filters = filters
        self.pagination = pagination
