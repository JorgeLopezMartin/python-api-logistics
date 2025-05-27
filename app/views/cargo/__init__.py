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
from app.schemas.cargo import (
    CargoRequest,
    CargoResponse,
    CargoResponseDuplicated,
    CargoResponseNotDeletable,
    CargoResponseNotFound
)
from app.schemas.contract import ContractResponseNotFound
from app.views.cargo.create_cargo import create_cargo
from app.views.cargo.delete_cargo import delete_cargo
from app.views.cargo.get_cargo import get_cargo
from app.views.cargo.list_cargoes import list_cargoes
from app.views.cargo.update_cargo import update_cargo

TAG = 'cargoes'

cargoes_router = APIRouter()

cargoes_router.add_api_route(
    endpoint=create_cargo,
    methods=['POST'],
    name='create_cargo',
    path='',
    response_model=APIResponse[CargoResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ContractResponseNotFound]
        },
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[CargoResponseDuplicated]
        },
    },
    status_code=HTTP_201_CREATED,
    summary='Create a new cargo',
    tags=[TAG]
)

cargoes_router.add_api_route(
    endpoint=get_cargo,
    methods=['GET'],
    name='get_cargo',
    path='/{cargo_id}',
    response_model=APIResponse[CargoResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[CargoResponseNotFound]
        }
    },
    status_code=HTTP_200_OK,
    summary='Retrieve cargo info by ID.',
    tags=[TAG]
)

cargoes_router.add_api_route(
    endpoint=list_cargoes,
    methods=['GET'],
    name='list_cargoes',
    path='',
    response_model=APIResponsePaginated[CargoResponse],
    status_code=HTTP_200_OK,
    summary='Retrieves cargoes applying filters.',
    tags=[TAG]
)

cargoes_router.add_api_route(
    endpoint=delete_cargo,
    methods=['DELETE'],
    name='delete_cargo',
    path='/{cargo_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[CargoResponseNotFound]
        },
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[CargoResponseNotDeletable]
        }
    },
    summary='Deletes a specific cargo by ID.',
    tags=[TAG]
)

cargoes_router.add_api_route(
    endpoint=update_cargo,
    methods=['PATCH'],
    name='update_cargo',
    path='/{cargo_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[CargoResponseNotFound]
        }
    },
    summary='Updates an existing cargo',
    tags=[TAG]
)
