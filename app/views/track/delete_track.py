import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from starlette.responses import Response

from app.services.track import TrackService
from app.schemas.track import (
    TrackResponseNotDeletable,
    TrackResponseNotFound
)
from app.services.exceptions import (
    TrackNotDeletableException,
    TrackNotFoundException
)
from app.views.exceptions import raise_http_exception


logger = logging.getLogger(__name__)

def delete_track(
    track_id: int,
    track_service: TrackService = Depends()
) -> Response:
    """Endpoint for deleting tracking information"""
    logger.info('Deleting track %s', track_id)
    try:
        track_service.delete(track_id)
        logger.info('Track %s deleted', track_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except TrackNotDeletableException as ex:
        logger.info('Track %s cannot be deleted', track_id)
        return raise_http_exception(ex, HTTP_409_CONFLICT, [TrackResponseNotDeletable().dict()])
    except TrackNotFoundException as ex:
        logger.info('Track %s cannot be found', track_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [TrackResponseNotFound().dict()])
