import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from starlette.responses import Response

from app.services.contract import ContractService
from app.schemas.contract import (
    ContractResponseNotDeletable,
    ContractResponseNotFound
)
from app.services.exceptions import (
    ContractNotDeletableException,
    ContractNotFoundException
)
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)

def delete_contract(
    contract_id: int,
    contract_service: ContractService = Depends()
) -> Response:
    """Endpoint function for deleting a contract"""
    logger.info('Deleting contract %s', contract_id)
    try:
        contract_service.delete(contract_id)
        logger.info('Contract %s deleted', contract_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except ContractNotDeletableException as ex:
        logger.info('Contract %s cannot be deleted', contract_id)
        return raise_http_exception(ex, HTTP_409_CONFLICT, [ContractResponseNotDeletable().dict()])
    except ContractNotFoundException as ex:
        logger.info('Contract %s not found', contract_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ContractResponseNotFound().dict()])
