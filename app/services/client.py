from fastapi.param_functions import Depends

from app.database.query import Page
from app.models.client import Client
from app.repositories.client import ClientRepository
from app.repositories.exceptions import DuplicateException, NotFoundException
from app.schemas.params.client import ClientParams
from app.services.exceptions import ClientDuplicatedException, ClientNotFoundException


class ClientService:
    """Application service to manage Clients"""

    def __init__(
        self,
        client_repository: ClientRepository = Depends()
    ) -> None:
        self.client_repository = client_repository

    def get(
        self,
        id: int
    ) -> Client:
        """Retrieve a Client
        
        :raises 'ClientNotFoundException': Client ID not found in DB
        """
        try:
            with self.client_repository:
                return self.client_repository.get(id=id)
        except NotFoundException as ex:
            raise ClientNotFoundException() from ex

    def create(
        self,
        name: str
    ) -> Client:
        """Creates a new client"""
        try:
            return self.client_repository.create(
                name=name
            )
        except DuplicateException as ex:
            raise ClientDuplicatedException() from ex

    def list(self, params: ClientParams) -> Page[Client]:
        """Retrieves clients. Response is paginated"""

        return self.client_repository.list(params)

    def delete(self, client_id: int) -> None:
        """Deletes an already existing client"""

        try:
            with self.client_repository:
                client = self.client_repository.get(id=client_id)
                self.client_repository.delete(client)
        except NotFoundException as ex:
            raise ClientNotFoundException() from ex

    def update(
        self,
        client_id: int,
        **kwargs
    ) -> None:
        try:
            with self.client_repository:
                location = self.client_repository.get(id=client_id)
                if location:
                    self.client_repository.patch(location, **kwargs)
        except NotFoundException as ex:
            raise ClientNotFoundException() from ex