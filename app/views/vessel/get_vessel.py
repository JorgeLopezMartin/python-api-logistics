from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.vessel import VesselService
from app.schemas.base import APIResponse
from app.schemas.vessel import (
    VesselResponse,
    VesselResponseNotFound
)
from app.services.exceptions import VesselNotFoundException
from app.views.exceptions import raise_http_exception


def get_vessel(
    vessel_id: int,
    vessel_service: VesselService = Depends()
) -> APIResponse[VesselResponse]:
    """Endpoint function for finding a vessel by ID"""
    try:
        vessel = vessel_service.get(id=vessel_id)
        return APIResponse(data=vessel)
    except VesselNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [VesselResponseNotFound().dict()])
