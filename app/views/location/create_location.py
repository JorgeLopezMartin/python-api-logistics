import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_409_CONFLICT
)

from app.services.location import LocationService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.location import (
    LocationRequest,
    LocationResponse,
    LocationResponseDuplicated
)
from app.services.exceptions import LocationDuplicatedException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def create_location(
    request: APIRequest[LocationRequest],
    location_service: LocationService = Depends()
) -> APIResponse[LocationResponse]:
    """Endpoint function for creating a location"""
    logger.info('Creating new location')
    try:
        location = location_service.create(
            name=request.data.name,
            latitude=request.data.latitude,
            longitude=request.data.longitude
        )
        logger.info('New location created successfully')
        return APIResponse(data=location)
    except LocationDuplicatedException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [LocationResponseDuplicated().dict()])
