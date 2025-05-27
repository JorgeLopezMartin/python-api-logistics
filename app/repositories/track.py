from datetime import datetime
from typing import Any, Optional

from app.database.filter import QueryFilter
from app.database.query import Page
from app.models.track import Track
from app.repositories.base import BaseRepository
from app.schemas.params.track import TrackParams

class TrackRepository(BaseRepository):

    def create(
        self,
        date: datetime,
        location_id: int,
        cargo_id: Optional[int],
        vessel_id: int
    ) -> Track:
        "Create new tracking info"

        with self:
            new_track = Track(
                date=date,
                location_id=location_id,
                cargo_id=cargo_id,
                vessel_id=vessel_id
            )
            self.persist(new_track)
            return new_track

    def get(
        self,
        **filters: Any
    ) -> Track:
        """Find track given certain criteria
        
        :raises `NotFoundException`: Track not found.
        """
        return super().get(Track, **filters)

    def list(
        self,
        params: TrackParams
    ) -> Page[Track]:
        """Returns the tracks that match the given criteria"""

        q_filter = QueryFilter()

        q_filter.equal(Track.location_id, params.filters.location_id)
        q_filter.equal(Track.vessel_id, params.filters.vessel_id)
        q_filter.equal(Track.cargo_id, params.filters.cargo_id)

        query = self.query(Track).filter(q_filter())

        page = query.paginate(
            params.pagination.page,
            params.pagination.page_size
        )

        return page
