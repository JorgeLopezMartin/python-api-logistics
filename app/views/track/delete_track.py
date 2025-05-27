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


def delete_track(
    track_id: int,
    track_service: TrackService = Depends()
) -> Response:
    try:
        track_service.delete(track_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except TrackNotDeletableException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [TrackResponseNotDeletable().dict()])
    except TrackNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [TrackResponseNotFound().dict()])
