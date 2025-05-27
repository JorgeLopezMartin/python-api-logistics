import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.services.track import TrackService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.cargo import (
    CargoResponseAlreadyDelivered,
    CargoResponseNotFound
)
from app.schemas.location import LocationResponseNotFound
from app.schemas.track import (
    TrackRequest,
    TrackResponse,
    TrackResponseDuplicated
)
from app.schemas.vessel import VesselResponseNotFound
from app.services.exceptions import (
    CargoAlreadyDeliveredException,
    CargoNotFoundException,
    LocationNotFoundException,
    TrackDuplicatedException,
    VesselNotFoundException
)
from app.views.exceptions import raise_http_exception


logger = logging.getLogger(__name__)

def create_track(
    request: APIRequest[TrackRequest],
    track_service: TrackService = Depends()
) -> APIResponse[TrackResponse]:
    try:
        logger.info('Creating new track')
        track = track_service.create(
            date=request.data.date,
            location_id=request.data.location_id,
            cargo_id=request.data.cargo_id,
            vessel_id=request.data.vessel_id
        )
        return APIResponse(data=track)
    except CargoAlreadyDeliveredException as ex:
        return raise_http_exception(
            ex,
            HTTP_404_NOT_FOUND,
            [CargoResponseAlreadyDelivered().dict()]
        )
    except CargoNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [CargoResponseNotFound().dict()])
    except LocationNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [LocationResponseNotFound().dict()])
    except TrackDuplicatedException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [TrackResponseDuplicated().dict()])
    except VesselNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [VesselResponseNotFound().dict()])
