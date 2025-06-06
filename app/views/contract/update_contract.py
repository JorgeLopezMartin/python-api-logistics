import logging

from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.contract import ContractService
from app.schemas.base import APIRequest
from app.schemas.contract import (
    ContractUpdateRequest,
    ContractResponseNotFound
)
from app.services.exceptions import ContractNotFoundException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def update_contract(
    contract_id: int,
    request: APIRequest[ContractUpdateRequest],
    contract_service: ContractService = Depends()
) -> Response:
    """Endpoint function for updating a contract"""
    logger.info('Updating contract %s', contract_id)
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        contract_service.update(
            contract_id=contract_id,
            **update_params
        )
        logger.info('Contract %s updated', contract_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except ContractNotFoundException as ex:
        logger.info('Contract %s not found', contract_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ContractResponseNotFound().dict()])
