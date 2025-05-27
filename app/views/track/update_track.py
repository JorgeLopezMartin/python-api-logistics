from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.track import TrackService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.track import (
    TrackUpdateRequest,
    TrackResponse,
    TrackResponseNotFound
)
from app.services.exceptions import TrackNotFoundException
from app.views.exceptions import raise_http_exception


def update_track(
    track_id: int,
    request: APIRequest[TrackUpdateRequest],
    track_service: TrackService = Depends()
) -> Response:
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        track = track_service.update(
            track_id=track_id,
            **update_params
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except TrackNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [TrackResponseNotFound().dict()])
