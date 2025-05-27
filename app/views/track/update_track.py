import logging

from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.track import TrackService
from app.schemas.base import APIRequest
from app.schemas.track import (
    TrackUpdateRequest,
    TrackResponseNotFound
)
from app.services.exceptions import TrackNotFoundException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def update_track(
    track_id: int,
    request: APIRequest[TrackUpdateRequest],
    track_service: TrackService = Depends()
) -> Response:
    """Endpoint for updating a track"""
    logger.info('Updating track %s', track_id)
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        track_service.update(
            track_id=track_id,
            **update_params
        )
        logger.info('Track %s updated', track_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except TrackNotFoundException as ex:
        logger.info('Track %s not found', track_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [TrackResponseNotFound().dict()])
