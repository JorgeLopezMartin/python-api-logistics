from dataclasses import dataclass
from typing import Optional
from fastapi import Depends, Query

from app.schemas.params.pagination.pagination import PaginationParams


@dataclass
class ContractFilters:
    """Query parameters for filtering contracts"""

    client_id: Optional[int] = Query(None)
    location_id: Optional[int] = Query(None)


class ContractParams:
    """Query parameters for listing contracts"""

    def __init__ (
        self,
        filters: ContractFilters = Depends(),
        pagination: PaginationParams = Depends()
    ) -> None:
        self.filters = filters
        self.pagination = pagination
