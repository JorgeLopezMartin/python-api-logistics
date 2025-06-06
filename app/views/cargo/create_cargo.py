import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.services.cargo import CargoService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.cargo import (
    CargoRequest,
    CargoResponse,
    CargoResponseDuplicated
)
from app.schemas.contract import ContractResponseNotFound
from app.services.exceptions import (
    ContractNotFoundException,
    CargoDuplicatedException
)
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def create_cargo(
    request: APIRequest[CargoRequest],
    cargo_service: CargoService = Depends()
) -> APIResponse[CargoResponse]:
    """Defines endpoint function for POST /cargo.
    Creates a cargo in DB. Returns OK if successful.
    Returns 404 if assigned contract is not found."""
    try:
        logger.info('Creating new cargo')
        cargo = cargo_service.create(
            type=request.data.type,
            quantity=request.data.quantity,
            contract_id=request.data.contract_id
        )
        logger.info('Cargo created successfully')
        return APIResponse(data=cargo)
    except ContractNotFoundException as ex:
        logger.info('Contract %s not found', request.data.contract_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ContractResponseNotFound().dict()])
    except CargoDuplicatedException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [CargoResponseDuplicated().dict()])
