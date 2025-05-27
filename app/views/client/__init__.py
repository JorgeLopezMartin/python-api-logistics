from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_502_BAD_GATEWAY
)

from app.schemas.base import (
    APIErrorResponse,
    APIResponse,
    APIResponsePaginated
)
from app.schemas.client import (
    ClientRequest,
    ClientResponse,
    ClientResponseDuplicated,
    ClientResponseNotDeletable,
    ClientResponseNotFound
)
from app.views.client.create_client import create_client
from app.views.client.delete_client import delete_client
from app.views.client.get_client import get_client
from app.views.client.list_clients import list_clients
from app.views.client.update_client import update_client

TAG = 'clients'

clients_router = APIRouter()

clients_router.add_api_route(
    endpoint=create_client,
    methods=['POST'],
    name='create_client',
    path='',
    response_model=APIResponse[ClientResponse],
    responses={
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[ClientResponseDuplicated]
        },
    },
    status_code=HTTP_201_CREATED,
    summary='Create a new client',
    tags=[TAG]
)

clients_router.add_api_route(
    endpoint=get_client,
    methods=['GET'],
    name='get_client',
    path='/{client_id}',
    response_model=APIResponse[ClientResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ClientResponseNotFound]
        }
    },
    status_code=HTTP_200_OK,
    summary='Retrieve client info by ID.',
    tags=[TAG]
)

clients_router.add_api_route(
    endpoint=list_clients,
    methods=['GET'],
    name='list_clients',
    path='',
    response_model=APIResponsePaginated[ClientResponse],
    status_code=HTTP_200_OK,
    summary='Retrieves clients applying filters.',
    tags=[TAG]
)

clients_router.add_api_route(
    endpoint=delete_client,
    methods=['DELETE'],
    name='delete_client',
    path='/{client_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ClientResponseNotFound]
        },
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[ClientResponseNotDeletable]
        }
    },
    summary='Deletes a specific client by ID.',
    tags=[TAG]
)

clients_router.add_api_route(
    endpoint=update_client,
    methods=['PATCH'],
    name='update_client',
    path='/{client_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[ClientResponseNotFound]
        }
    },
    summary='Updates an existing client',
    tags=[TAG]
)