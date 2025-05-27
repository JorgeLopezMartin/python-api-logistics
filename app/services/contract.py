from fastapi.param_functions import Depends

from app.database.query import Page
from app.models.contract import Contract
from app.repositories.exceptions import (
    DeleteException,
    DuplicateException,
    NotFoundException
)
from app.repositories.client import ClientRepository
from app.repositories.contract import ContractRepository
from app.repositories.location import LocationRepository
from app.schemas.params.contract import ContractParams
from app.services.exceptions import (
    ClientNotFoundException,
    ContractDuplicatedException,
    ContractNotDeletableException,
    ContractNotFoundException,
    LocationNotFoundException
)


class ContractService:
    """Application service to manage contracts"""

    def __init__(
        self,
        client_repository: ClientRepository = Depends(),
        contract_repository: ContractRepository = Depends(),
        location_repository: LocationRepository = Depends()
    ) -> None:
        self.client_repository = client_repository
        self.contract_repository = contract_repository
        self.location_repository = location_repository

    def get(
        self,
        id: int
    ) -> Contract:
        """Retrieve the Contract
        
        :raises 'ContractNotFoundException': Contract not found in DB.
        """
        try:
            with self.contract_repository:
                return self.contract_repository.get(id=id)
        except NotFoundException as ex:
            raise ContractNotFoundException() from ex

    def create(
        self,
        price: float,
        client_id: int,
        location_id: int
    ) -> Contract:
        """Creates a new contract."""
        try:
            self.client_repository.get(id=client_id)
        except NotFoundException as ex:
            raise ClientNotFoundException() from ex

        try:
            self.location_repository.get(id=location_id)
        except NotFoundException as ex:
            raise LocationNotFoundException() from ex

        try:
            return self.contract_repository.create(
                price=price,
                client_id=client_id,
                location_id=location_id
            )

        except DuplicateException as ex:
            raise ContractDuplicatedException() from ex

    def list(self, params: ContractParams) -> Page[Contract]:
        """Retrieves contracts. Response is paginated"""

        return self.contract_repository.list(params)

    def delete(self, contract_id: int) -> None:
        """Deletes an already existing contract"""

        try:
            with self.contract_repository:
                contract = self.contract_repository.get(id=contract_id)
                self.contract_repository.delete(contract)
        except DeleteException as ex:
            raise ContractNotDeletableException() from ex
        except NotFoundException as ex:
            raise ContractNotFoundException() from ex

    def update(
        self,
        contract_id: int,
        **kwargs
    ) -> None:
        try:
            with self.contract_repository:
                contract = self.contract_repository.get(id=contract_id)
                if contract:
                    self.contract_repository.patch(contract, **kwargs)
        except NotFoundException as ex:
            raise ContractNotFoundException() from ex