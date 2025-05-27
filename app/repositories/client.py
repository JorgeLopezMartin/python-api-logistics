from typing import Any

from app.database.filter import QueryFilter
from app.database.query import Page
from app.models.client import Client
from app.repositories.base import BaseRepository
from app.schemas.params.client import ClientParams

class ClientRepository(BaseRepository):

    def create(
        self,
        name: str
    ) -> Client:
        """Create a new client"""

        with self:
            new_client = Client(
                name=name
            )
            self.persist(new_client)
            return new_client

    def get(  # pylint: disable=arguments-differ
        self,
        **filters: Any
    ) -> Client:
        """Find client given certain criteria
        
        :raises 'NotFoundException': Client not found
        """
        return super().get(Client, **filters)

    def list(
        self,
        params: ClientParams
    ) -> Page[Client]:
        """Returns the clients that match the given criteria"""

        q_filter = QueryFilter()

        q_filter.ilike(Client.name, params.filters.name)

        query = self.query(Client).filter(q_filter())

        page = query.paginate(
            params.pagination.page,
            params.pagination.page_size
        )

        return page
