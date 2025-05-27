import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.location import LocationService
from app.schemas.base import APIResponse
from app.schemas.location import (
    LocationResponse,
    LocationResponseNotFound
)
from app.services.exceptions import LocationNotFoundException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def get_location(
    location_id: int,
    location_service: LocationService = Depends()
) -> APIResponse[LocationResponse]:
    """Endpoint function for retrieving a location by ID"""
    logger.info('Searching location %s', location_id)
    try:
        location = location_service.get(id=location_id)
        logger.info('Retrieved location %s', location_id)
        return APIResponse(data=location)
    except LocationNotFoundException as ex:
        logger.info('Location %s not found', location_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [LocationResponseNotFound().dict()])
