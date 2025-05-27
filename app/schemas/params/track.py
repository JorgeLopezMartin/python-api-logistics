from dataclasses import dataclass
from typing import Optional
from fastapi import Depends, Query

from app.schemas.params.pagination.pagination import PaginationParams


@dataclass
class TrackFilters:
    """Query parameters for filtering contracts"""

    location_id: Optional[int] = Query(None)
    cargo_id: Optional[int] = Query(None)
    vessel_id: Optional[int] = Query(None)

class TrackParams:
    """Query parameters for listing contracts"""

    def __init__ (
        self,
        filters: TrackFilters = Depends(),
        pagination: PaginationParams = Depends()
    ) -> None:
        self.filters = filters
        self.pagination = pagination