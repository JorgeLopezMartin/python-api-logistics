import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.services.contract import ContractService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.client import ClientResponseNotFound
from app.schemas.contract import (
    ContractRequest,
    ContractResponse,
    ContractResponseDuplicated
)
from app.schemas.location import LocationResponseNotFound
from app.services.exceptions import (
    ClientNotFoundException,
    ContractDuplicatedException,
    LocationNotFoundException
)
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)

def create_contract(
    request: APIRequest[ContractRequest],
    contract_service: ContractService = Depends()
) -> APIResponse[ContractResponse]:
    """Endpoint function for creating a contract"""
    try:
        logger.info('Creating new contract')
        contract = contract_service.create(
            price=request.data.price,
            client_id=request.data.client_id,
            location_id=request.data.location_id
        )
        logger.info('Contract successfully created')
        return APIResponse(data=contract)
    except ClientNotFoundException as ex:
        logger.info('Client %s not found', request.data.client_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ClientResponseNotFound().dict()])
    except ContractDuplicatedException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [ContractResponseDuplicated().dict()])
    except LocationNotFoundException as ex:
        logger.info('Location %s not found', request.data.location_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [LocationResponseNotFound().dict()])
