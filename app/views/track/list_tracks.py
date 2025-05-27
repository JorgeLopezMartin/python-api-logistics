from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends

from app.services.track import TrackService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.track import TrackParams
from app.schemas.track import TrackResponse

from app.views.exceptions import raise_http_exception


def list_tracks(
    params: TrackParams = Depends(),
    track_service: TrackService = Depends()
) -> APIResponsePaginated[TrackResponse]:
    """List existing tracks"""

    page = track_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)