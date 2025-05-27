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
from app.schemas.vessel import (
    VesselRequest,
    VesselResponse,
    VesselResponseDuplicated,
    VesselResponseNotFound
)
from app.views.vessel.create_vessel import create_vessel
from app.views.vessel.delete_vessel import delete_vessel
from app.views.vessel.get_vessel import get_vessel
from app.views.vessel.list_vessels import list_vessels
from app.views.vessel.update_vessel import update_vessel

TAG = 'vessels'

vessels_router = APIRouter()

vessels_router.add_api_route(
    endpoint=create_vessel,
    methods=['POST'],
    name='create_vessel',
    path='',
    response_model=APIResponse[VesselResponse],
    responses={
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[VesselResponseDuplicated]
        },
    },
    status_code=HTTP_201_CREATED,
    summary='Create a new vessel',
    tags=[TAG]
)

vessels_router.add_api_route(
    endpoint=get_vessel,
    methods=['GET'],
    name='get_vessel',
    path='/{vessel_id}',
    response_model=APIResponse[VesselResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[VesselResponseNotFound]
        }
    },
    status_code=HTTP_200_OK,
    summary='Retrieve vessel info by ID.',
    tags=[TAG]
)

vessels_router.add_api_route(
    endpoint=list_vessels,
    methods=['GET'],
    name='list_vessels',
    path='',
    response_model=APIResponsePaginated[VesselResponse],
    status_code=HTTP_200_OK,
    summary='Retrieves vessels applying filters.',
    tags=[TAG]
)

vessels_router.add_api_route(
    endpoint=delete_vessel,
    methods=['DELETE'],
    name='delete_vessel',
    path='/{vessel_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[VesselResponseNotFound]
        }
    },
    summary='Deletes a specific vessel by ID.',
    tags=[TAG]
)

vessels_router.add_api_route(
    endpoint=update_vessel,
    methods=['PATCH'],
    name='update_vessel',
    path='/{vessel_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[VesselResponseNotFound]
        }
    },
    summary='Updates an existing vessel',
    tags=[TAG]
)
