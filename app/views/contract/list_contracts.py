import logging

from fastapi.params import Depends

from app.services.contract import ContractService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.contract import ContractParams
from app.schemas.contract import ContractResponse

logger = logging.getLogger(__name__)


def list_contracts(
    params: ContractParams = Depends(),
    contract_service: ContractService = Depends()
) -> APIResponsePaginated[ContractResponse]:
    """List existing contracts"""
    logger.info('Listing contracts')
    page = contract_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)
