from typing import Any

from app.database.filter import QueryFilter
from app.database.query import Page
from app.models.contract import Contract
from app.repositories.base import BaseRepository
from app.schemas.params.contract import ContractParams

class ContractRepository(BaseRepository):

    def create(
        self,
        price: float,
        client_id: int,
        location_id: int
    ) -> Contract:
        "Create a new contract"

        with self:
            new_contract = Contract(
                price=price,
                client_id=client_id,
                location_id=location_id
            )
            self.persist(new_contract)
            return new_contract

    def get(  # pylint: disable=arguments-differ
        self,
        **filters: Any
    ) -> Contract:
        """Find contract given certain criteria
        
        :raises `NotFoundException`: Contract not found.
        """
        return super().get(Contract, **filters)

    def list(
        self,
        params: ContractParams
    ) -> Page[Contract]:
        """Returns the locations that match the given criteria"""

        q_filter = QueryFilter()

        q_filter.equal(Contract.client_id, params.filters.client_id)
        q_filter.equal(Contract.location_id, params.filters.location_id)

        query = self.query(Contract).filter(q_filter())

        page = query.paginate(
            params.pagination.page,
            params.pagination.page_size
        )

        return page
