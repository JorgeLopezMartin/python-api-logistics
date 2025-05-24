from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_502_BAD_GATEWAY,
)

from app.schemas.base import APIErrorResponse, APIResponse
from app.schemas.location import (
    LocationRequest,
    LocationResponse
)
from app.views.location.create_location import create_location

TAG = 'locations'

locations_router = APIRouter()

locations_router.add_api_route(
    endpoint=create_location,
    methods=['POST'],
    name='create',
    path='',
    response_model=APIResponse[LocationResponse],
    responses={
    },
    status_code=HTTP_201_CREATED,
    summary='Create a new location',
    tags=[TAG]
)