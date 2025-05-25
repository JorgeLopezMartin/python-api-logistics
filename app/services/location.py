from fastapi.param_functions import Depends

from app.database.query import Page
from app.models.location import Location
from app.repositories.exceptions import DuplicateException, NotFoundException
from app.repositories.location import LocationRepository
from app.schemas.params.location import LocationParams
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

    def list(self, params: LocationParams) -> Page[Location]:
        """Retrieves locations. Response is paginated"""

        return self.location_repository.list(params)

    def delete(self, location_id: int) -> None:
        """Deletes an already existing location"""

        try:
            with self.location_repository:
                location = self.location_repository.get(id=location_id)
                self.location_repository.delete(location)
        except NotFoundException as ex:
            raise LocationNotFoundException() from ex

    def update(
        self,
        location_id: int,
        **kwargs
    ) -> None:
        try:
            with self.location_repository:
                location = self.location_repository.get(id=location_id)
                if location:
                    self.location_repository.patch(location, **kwargs)
        except NotFoundException as ex:
            raise LocationNotFoundException() from ex