# pylint: disable=redefined-builtin
from typing import Any

from app.database.filter import QueryFilter
from app.database.query import Page
from app.models.cargo import (
    Cargo,
    CargoStatus,
    CargoType
)
from app.repositories.base import BaseRepository
from app.schemas.params.cargo import CargoParams

class CargoRepository(BaseRepository):

    def create(
        self,
        type: CargoType,
        quantity: float,
        contract_id: int
    ) -> Cargo:
        "Create a new cargo"

        with self:
            new_cargo = Cargo(
                type=type,
                quantity=quantity,
                status=CargoStatus.pending,
                contract_id=contract_id
            )
            self.persist(new_cargo)
            return new_cargo

    def get(  # pylint: disable=arguments-differ
        self,
        **filters: Any
    ) -> Cargo:
        """Find cargo given certain criteria
        
        :raises `NotFoundException`: Cargo not found.
        """
        return super().get(Cargo, **filters)

    def list(
        self,
        params: CargoParams
    ) -> Page[Cargo]:
        """Returns the cargoes that match the given criteria"""

        q_filter = QueryFilter()

        q_filter.equal(Cargo.type, params.filters.type)
        q_filter.equal(Cargo.status, params.filters.status)
        q_filter.equal(Cargo.contract_id, params.filters.contract_id)

        query = self.query(Cargo).filter(q_filter())

        page = query.paginate(
            params.pagination.page,
            params.pagination.page_size
        )

        return page
