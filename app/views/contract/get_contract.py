import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.contract import ContractService
from app.schemas.base import APIResponse
from app.schemas.contract import (
    ContractResponse,
    ContractResponseNotFound
)
from app.services.exceptions import ContractNotFoundException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)

def get_contract(
    contract_id: int,
    contract_service: ContractService = Depends()
) -> APIResponse[ContractResponse]:
    """Endpoint function for finding a contract by ID"""
    logger.info('Searching contract %s', contract_id)
    try:
        contract = contract_service.get(id=contract_id)
        logger.info('Contract %s retrieved', contract_id)
        return APIResponse(data=contract)
    except ContractNotFoundException as ex:
        logger.info('Contract %s not found', contract_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ContractResponseNotFound().dict()])
