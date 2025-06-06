import logging

from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.location import LocationService
from app.schemas.base import APIRequest
from app.schemas.location import (
    LocationUpdateRequest,
    LocationResponseNotFound
)
from app.services.exceptions import LocationNotFoundException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def update_location(
    location_id: int,
    request: APIRequest[LocationUpdateRequest],
    location_service: LocationService = Depends()
) -> Response:
    """Endpoint function for updating a location"""
    logger.info('Updating location %s', location_id)
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        location_service.update(
            location_id=location_id,
            **update_params
        )
        logger.info('Location %s updated', location_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except LocationNotFoundException as ex:
        logger.info('Location %s not found', location_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [LocationResponseNotFound().dict()])
