from fastapi.param_functions import Depends

from app.database.query import Page
from app.models.cargo import (
    Cargo,
    CargoStatus,
    CargoType
)
from app.repositories.exceptions import (
    DeleteException,
    DuplicateException,
    NotFoundException
)
from app.repositories.cargo import CargoRepository
from app.repositories.contract import ContractRepository
from app.schemas.params.cargo import CargoParams
from app.services.exceptions import (
    CargoDuplicatedException,
    CargoNotDeletableException,
    CargoNotFoundException,
    ContractNotFoundException
)


class CargoService:
    """Application service to manage cargoes"""

    def __init__(
        self,
        cargo_repository: CargoRepository = Depends(),
        contract_repository: ContractRepository = Depends()
    ) -> None:
        self.cargo_repository = cargo_repository
        self.contract_repository = contract_repository

    def get(
        self,
        id: int
    ) -> Cargo:
        """Retrieve the Cargo
        
        :raises 'CargoNotFoundException': Cargo not found in DB.
        """
        try:
            with self.cargo_repository:
                return self.cargo_repository.get(id=id)
        except NotFoundException as ex:
            raise CargoNotFoundException() from ex

    def create(
        self,
        type: CargoType,
        quantity: float,
        contract_id: int
    ) -> Cargo:
        """Creates a new cargo."""
        try:
            self.contract_repository.get(id=contract_id)
        except NotFoundException as ex:
            raise ContractNotFoundException() from ex

        try:
            return self.cargo_repository.create(
                type=type,
                quantity=quantity,
                contract_id=contract_id
            )

        except DuplicateException as ex:
            raise CargoDuplicatedException() from ex

    def list(self, params: CargoParams) -> Page[Cargo]:
        """Retrieves cargoes. Response is paginated"""

        return self.cargo_repository.list(params)

    def delete(self, cargo_id: int) -> None:
        """Deletes an already existing cargo"""

        try:
            with self.cargo_repository:
                cargo = self.cargo_repository.get(id=cargo_id)
                self.cargo_repository.delete(cargo)
        except DeleteException as ex:
            raise CargoNotDeletableException() from ex
        except NotFoundException as ex:
            raise CargoNotFoundException() from ex

    def update(
        self,
        cargo_id: int,
        **kwargs
    ) -> None:
        """Updated an existing cargo"""
        try:
            with self.cargo_repository:
                cargo = self.cargo_repository.get(id=cargo_id)
                if cargo:
                    self.cargo_repository.patch(cargo, **kwargs)
        except NotFoundException as ex:
            raise CargoNotFoundException() from ex