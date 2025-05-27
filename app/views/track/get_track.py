import logging

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.track import TrackService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.track import (
    TrackRequest,
    TrackResponse,
    TrackResponseNotFound
)
from app.services.exceptions import TrackNotFoundException
from app.settings import get_settings
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)

def get_track(
    track_id: int,
    track_service: TrackService = Depends()
) -> APIResponse[TrackResponse]:
    try:
        track = track_service.get(id=track_id)
        return APIResponse(data=track)
    except TrackNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [TrackResponseNotFound().dict()])
