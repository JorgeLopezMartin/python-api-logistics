from fastapi.param_functions import Depends

from app.database.query import Page
from app.models.vessel import Vessel
from app.repositories.exceptions import (
    DeleteException,
    DuplicateException,
    NotFoundException
)
from app.repositories.vessel import VesselRepository
from app.schemas.params.vessel import VesselParams
from app.services.exceptions import (
    VesselDuplicatedException,
    VesselNotDeletableException,
    VesselNotFoundException
)


class VesselService:
    """Application service to manage Vessels"""

    def __init__(
        self,
        vessel_repository: VesselRepository = Depends()
    ) -> None:
        self.vessel_repository = vessel_repository

    def get(
        self,
        id: int
    ) -> Vessel:
        """Retrieve the Vessel
        
        :raises 'VesselNotFoundException': Vessel not found in DB.
        """
        try:
            with self.vessel_repository:
                return self.vessel_repository.get(id=id)
        except NotFoundException as ex:
            raise VesselNotFoundException() from ex

    def create(
        self,
        name: str,
        capacity: float
    ) -> Vessel:
        """Creates a new vessel."""
        try:
            return self.vessel_repository.create(
                name=name,
                capacity=capacity
            )

        except DuplicateException as ex:
            raise VesselDuplicatedException() from ex

    def list(self, params: VesselParams) -> Page[Vessel]:
        """Retrieves vessels. Response is paginated"""

        return self.vessel_repository.list(params)

    def delete(self, vessel_id: int) -> None:
        """Deletes an already existing vessel"""

        try:
            with self.vessel_repository:
                vessel = self.vessel_repository.get(id=vessel_id)
                self.vessel_repository.delete(vessel)
        except DeleteException as ex:
            raise VesselNotDeletableException() from ex
        except NotFoundException as ex:
            raise VesselNotFoundException() from ex

    def update(
        self,
        vessel_id: int,
        **kwargs
    ) -> None:
        try:
            with self.vessel_repository:
                vessel = self.vessel_repository.get(id=vessel_id)
                if vessel:
                    self.vessel_repository.patch(vessel, **kwargs)
        except NotFoundException as ex:
            raise VesselNotFoundException() from ex