import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.track import TrackService
from app.schemas.base import APIResponse
from app.schemas.track import (
    TrackResponse,
    TrackResponseNotFound
)
from app.services.exceptions import TrackNotFoundException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)

def get_track(
    track_id: int,
    track_service: TrackService = Depends()
) -> APIResponse[TrackResponse]:
    """Endpoint for finding a track by ID"""
    logger.info('Searching track %s', track_id)
    try:
        track = track_service.get(id=track_id)
        logger.info('Track %s found', track_id)
        return APIResponse(data=track)
    except TrackNotFoundException as ex:
        logger.info('Track %s not found', track_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [TrackResponseNotFound().dict()])
