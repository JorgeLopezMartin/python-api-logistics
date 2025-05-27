from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_502_BAD_GATEWAY,
)

from app.schemas.base import (
    APIErrorResponse,
    APIResponse,
    APIResponsePaginated
)
from app.schemas.client import ClientResponseNotFound
from app.schemas.contract import (
    ContractRequest,
    ContractResponse,
    ContractResponseDuplicated,
    ContractResponseNotDeletable,
    ContractResponseNotFound
)
from app.schemas.location import LocationResponseNotFound
from app.views.contract.create_contract import create_contract
from app.views.contract.delete_contract import delete_contract
from app.views.contract.get_contract import get_contract
from app.views.contract.list_contracts import list_contracts
from app.views.contract.update_contract import update_contract

TAG = 'contracts'

contracts_router = APIRouter()

contracts_router.add_api_route(
    endpoint=create_contract,
    methods=['POST'],
    name='create_contract',
    path='',
    response_model=APIResponse[ContractResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ClientResponseNotFound|LocationResponseNotFound]
        },
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[ContractResponseDuplicated]
        },
    },
    status_code=HTTP_201_CREATED,
    summary='Create a new contract',
    tags=[TAG]
)

contracts_router.add_api_route(
    endpoint=get_contract,
    methods=['GET'],
    name='get_contract',
    path='/{contract_id}',
    response_model=APIResponse[ContractResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ContractResponseNotFound]
        }
    },
    status_code=HTTP_200_OK,
    summary='Retrieve contract info by ID.',
    tags=[TAG]
)

contracts_router.add_api_route(
    endpoint=list_contracts,
    methods=['GET'],
    name='list_contracts',
    path='',
    response_model=APIResponsePaginated[ContractResponse],
    status_code=HTTP_200_OK,
    summary='Retrieves contracts applying filters.',
    tags=[TAG]
)

contracts_router.add_api_route(
    endpoint=delete_contract,
    methods=['DELETE'],
    name='delete_contract',
    path='/{contract_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ContractResponseNotFound]
        },
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[ContractResponseNotDeletable]
        }
    },
    summary='Deletes a specific contract by ID.',
    tags=[TAG]
)

contracts_router.add_api_route(
    endpoint=update_contract,
    methods=['PATCH'],
    name='update_contract',
    path='/{contract_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ContractResponseNotFound]
        }
    },
    summary='Updated an existing contract',
    tags=[TAG]
)