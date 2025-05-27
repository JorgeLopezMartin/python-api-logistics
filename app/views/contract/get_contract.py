from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.contract import ContractService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.contract import (
    ContractRequest,
    ContractResponse,
    ContractResponseNotFound
)
from app.services.exceptions import ContractNotFoundException
from app.views.exceptions import raise_http_exception


def get_contract(
    contract_id: int,
    contract_service: ContractService = Depends()
) -> APIResponse[ContractResponse]:
    try:
        contract = contract_service.get(id=contract_id)
        return APIResponse(data=contract)
    except ContractNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [ContractResponseNotFound().dict()])
