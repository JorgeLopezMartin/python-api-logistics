from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from starlette.responses import Response

from app.services.vessel import VesselService
from app.schemas.vessel import (
    VesselResponseNotDeletable,
    VesselResponseNotFound
)
from app.services.exceptions import (
    VesselNotDeletableException,
    VesselNotFoundException
)
from app.views.exceptions import raise_http_exception


def delete_vessel(
    vessel_id: int,
    vessel_service: VesselService = Depends()
) -> Response:
    """Endpoint function for deleting a vessel by ID"""
    try:
        vessel_service.delete(vessel_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except VesselNotDeletableException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [VesselResponseNotDeletable().dict()])
    except VesselNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [VesselResponseNotFound().dict()])
