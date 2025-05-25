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
from app.schemas.location import (
    LocationRequest,
    LocationResponse,
    LocationResponseDuplicated,
    LocationResponseNotFound
)
from app.views.location.create_location import create_location
from app.views.location.delete_location import delete_location
from app.views.location.get_location import get_location
from app.views.location.list_locations import list_locations
from app.views.location.update_location import update_location

TAG = 'locations'

locations_router = APIRouter()

locations_router.add_api_route(
    endpoint=create_location,
    methods=['POST'],
    name='create_location',
    path='',
    response_model=APIResponse[LocationResponse],
    responses={
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[LocationResponseDuplicated]
        },
    },
    status_code=HTTP_201_CREATED,
    summary='Create a new location',
    tags=[TAG]
)

locations_router.add_api_route(
    endpoint=get_location,
    methods=['GET'],
    name='get_location',
    path='/{location_id}',
    response_model=APIResponse[LocationResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[LocationResponseNotFound]
        }
    },
    status_code=HTTP_200_OK,
    summary='Retrieve location info by ID.',
    tags=[TAG]
)

locations_router.add_api_route(
    endpoint=list_locations,
    methods=['GET'],
    name='list_locations',
    path='',
    response_model=APIResponsePaginated[LocationResponse],
    status_code=HTTP_200_OK,
    summary='Retrieves locations applying filters.',
    tags=[TAG]
)

locations_router.add_api_route(
    endpoint=delete_location,
    methods=['DELETE'],
    name='delete_location',
    path='/{location_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[LocationResponseNotFound]
        }
    },
    summary='Deletes a specific location by ID.',
    tags=[TAG]
)

locations_router.add_api_route(
    endpoint=update_location,
    methods=['PATCH'],
    name='update_location',
    path='/{location_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[LocationResponseNotFound]
        }
    },
    summary='Updated an existing location',
    tags=[TAG]
)
