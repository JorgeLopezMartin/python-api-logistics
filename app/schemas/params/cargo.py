from dataclasses import dataclass
from typing import Optional
from fastapi import Depends, Query

from app.models.cargo import CargoType, CargoStatus
from app.schemas.params.pagination.pagination import PaginationParams


@dataclass
class CargoFilters:
    """Query parameters for filtering cargoes"""

    type: Optional[CargoType] = Query(None)
    status: Optional[CargoStatus] = Query(None)
    contract_id: Optional[int] = Query(None)

class CargoParams:
    """Query parameters for listing cargoes"""

    def __init__(
        self,
        filters: CargoFilters = Depends(),
        pagination: PaginationParams = Depends()
    ) -> None:
        self.filters = filters
        self.pagination = pagination