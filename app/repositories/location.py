from typing import Any

from app.database.filter import QueryFilter
from app.database.query import Page
from app.models.location import Location
from app.repositories.base import BaseRepository
from app.schemas.params.location import LocationParams

class LocationRepository(BaseRepository):

    def create(
        self,
        name: str,
        latitude: float,
        longitude: float
    ) -> Location:
        "Create a new location"

        with self:
            new_location = Location(
                name=name,
                latitude=latitude,
                longitude=longitude
            )
            self.persist(new_location)
            return new_location

    def get(
        self,
        **filters: Any
    ) -> Location:
        """Find location given certain criteria
        
        :raises `NotFoundException`: Location not found.
        """
        return super().get(Location, **filters)

    def list(
        self,
        params: LocationParams
    ) -> Page[Location]:
        """Returns the locations that match the given criteria"""

        q_filter = QueryFilter()

        q_filter.ilike(Location.name, params.filters.name)

        query = self.query(Location).filter(q_filter())

        page = query.paginate(
            params.pagination.page,
            params.pagination.page_size
        )

        return page