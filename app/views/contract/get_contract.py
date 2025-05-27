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


def get_contract(
    contract_id: int,
    contract_service: ContractService = Depends()
) -> APIResponse[ContractResponse]:
    """Endpoint function for finding a contract by ID"""
    try:
        contract = contract_service.get(id=contract_id)
        return APIResponse(data=contract)
    except ContractNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ContractResponseNotFound().dict()])
