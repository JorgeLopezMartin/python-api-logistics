import logging
from datetime import datetime
from typing import Optional

from fastapi.param_functions import Depends

from app.database.query import Page
from app.models.cargo import (
    CargoStatus
)
from app.models.track import Track
from app.repositories.exceptions import (
    DeleteException,
    DuplicateException,
    NotFoundException
)
from app.repositories.cargo import CargoRepository
from app.repositories.location import LocationRepository
from app.repositories.track import TrackRepository
from app.repositories.vessel import VesselRepository
from app.schemas.params.track import TrackParams
from app.services.exceptions import (
    CargoAlreadyDeliveredException,
    CargoNotFoundException,
    LocationNotFoundException,
    TrackDuplicatedException,
    TrackNotDeletableException,
    TrackNotFoundException,
    VesselNotFoundException
)
from app.settings import get_settings

logger = logging.getLogger(__name__)


class TrackService:
    """Application service to manage tracking information"""

    def __init__(
        self,
        cargo_repository: CargoRepository = Depends(),
        location_repository: LocationRepository = Depends(),
        track_repository: TrackRepository = Depends(),
        vessel_repository: VesselRepository = Depends()
    ) -> None:
        self.cargo_repository = cargo_repository
        self.location_repository = location_repository
        self.track_repository = track_repository
        self.vessel_repository = vessel_repository

    def get(
        self,
        id: int
    ) -> Track:
        """Retrieve the Track
        
        :raises 'TrackNotFoundException': Track not found in DB.
        """
        try:
            with self.track_repository:
                return self.track_repository.get(id=id)
        except NotFoundException as ex:
            raise TrackNotFoundException() from ex

    def create(
        self,
        date: datetime,
        location_id: int,
        cargo_id: Optional[int],
        vessel_id: int
    ) -> Track:
        """Creates a new piece of tracking information."""
        logger.info('Creating new track')
        try:
            self.location_repository.get(id=location_id)
        except NotFoundException as ex:
            raise LocationNotFoundException() from ex

        try:
            self.vessel_repository.get(id=vessel_id)
        except NotFoundException as ex:
            raise VesselNotFoundException() from ex

        cargo = None
        if cargo_id is not None:
            try:
                cargo = self.cargo_repository.get(id=cargo_id)
                if cargo.status == CargoStatus.delivered:
                    raise CargoAlreadyDeliveredException()
            except NotFoundException as ex:
                raise CargoNotFoundException() from ex

        try:
            track = self.track_repository.create(
                date=date,
                location_id=location_id,
                cargo_id=cargo_id,
                vessel_id=vessel_id
            )

        except DuplicateException as ex:
            raise TrackDuplicatedException() from ex

        if cargo_id is not None:
            logger.info('Cargo is present. Checking status to update')
            if cargo.contract.location_id == location_id:
                logger.info('Updating cargo to delivered status')
                with self.cargo_repository:
                    self.cargo_repository.patch(cargo, status=CargoStatus.delivered)
            elif cargo.status == CargoStatus.pending:
                logger.info('Updating cargo to in_transit status')
                with self.cargo_repository:
                    self.cargo_repository.patch(cargo, status=CargoStatus.in_transit)

        return track

    def list(self, params: TrackParams) -> Page[Track]:
        """Retrieves tracking information. Response is paginated"""

        return self.track_repository.list(params)

    def delete(self, track_id: int) -> None:
        """Deletes an already existing track"""

        try:
            with self.track_repository:
                track = self.track_repository.get(id=track_id)
                self.track_repository.delete(track)
        except DeleteException as ex:
            raise TrackNotDeletableException() from ex
        except NotFoundException as ex:
            raise TrackNotFoundException() from ex

    def update(
        self,
        track_id: int,
        **kwargs
    ) -> None:
        try:
            with self.track_repository:
                track = self.track_repository.get(id=track_id)
                if track:
                    self.track_repository.patch(track, **kwargs)
        except NotFoundException as ex:
            raise TrackNotFoundException() from ex