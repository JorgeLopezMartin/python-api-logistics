from typing import Any

from app.database.filter import QueryFilter
from app.database.query import Page
from app.models.vessel import Vessel
from app.repositories.base import BaseRepository
from app.schemas.params.vessel import VesselParams

class VesselRepository(BaseRepository):

    def create(
        self,
        name: str,
        capacity: float
    ) -> Vessel:
        "Create a new vessel"

        with self:
            new_vessel = Vessel(
                name=name,
                capacity=capacity
            )
            self.persist(new_vessel)
            return new_vessel

    def get(  # pylint: disable=arguments-differ
        self,
        **filters: Any
    ) -> Vessel:
        """Find vessel given certain criteria criteria
        
        :raises `NotFoundException`: Vessel not found.
        """
        return super().get(Vessel, **filters)

    def list(
        self,
        params: VesselParams
    ) -> Page[Vessel]:
        """Returns the vessels that match the given criteria"""

        q_filter = QueryFilter()

        q_filter.ilike(Vessel.name, params.filters.name)
        q_filter.between(Vessel.capacity, None, params.filters.capacity)

        query = self.query(Vessel).filter(q_filter())

        page = query.paginate(
            params.pagination.page,
            params.pagination.page_size
        )

        return page
