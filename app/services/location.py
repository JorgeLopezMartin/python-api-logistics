from fastapi.param_functions import Depends

from app.models.location import Location
from app.repositories.exceptions import DuplicateException, NotFoundException
from app.repositories.location import LocationRepository
from app.services.exceptions import LocationDuplicatedException, LocationNotFoundException


class LocationService:
    """Application service to manage Locations"""

    def __init__(
        self,
        location_repository: LocationRepository = Depends()
    ) -> None:
        self.location_repository = location_repository

    def get(
        self,
        id: int
    ) -> Location:
        """Retrieve the Location
        
        :raises 'LocationNotFoundException': Location not found in DB.
        """
        try:
            with self.location_repository:
                return self.location_repository.get(id=id)
        except NotFoundException as ex:
            raise LocationNotFoundException() from ex

    def create(
        self,
        name: str,
        latitude: float,
        longitude: float
    ) -> Location:
        """Creates a new location."""
        try:
            return self.location_repository.create(
                name=name,
                latitude=latitude,
                longitude=longitude
            )

        except DuplicateException as ex:
            raise LocationDuplicatedException() from ex