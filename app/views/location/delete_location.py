import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from starlette.responses import Response

from app.services.location import LocationService
from app.schemas.location import (
    LocationResponseNotDeletable,
    LocationResponseNotFound
)
from app.services.exceptions import (
    LocationNotDeletableException,
    LocationNotFoundException
)
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def delete_location(
    location_id: int,
    location_service: LocationService = Depends()
) -> Response:
    """Endpoint function for deleting a location by id"""
    logger.info('Deleting location %s', location_id)
    try:
        location_service.delete(location_id)
        logger.info('Location %s deleted', location_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except LocationNotDeletableException as ex:
        logger.info('Location %s not deletable', location_id)
        return raise_http_exception(ex, HTTP_409_CONFLICT, [LocationResponseNotDeletable().dict()])
    except LocationNotFoundException as ex:
        logger.info('Location %s not found', location_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [LocationResponseNotFound().dict()])
