import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_409_CONFLICT
)

from app.services.vessel import VesselService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.vessel import (
    VesselRequest,
    VesselResponse,
    VesselResponseDuplicated
)
from app.services.exceptions import VesselDuplicatedException
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def create_vessel(
    request: APIRequest[VesselRequest],
    vessel_service: VesselService = Depends()
) -> APIResponse[VesselResponse]:
    """Endpoint function for creating a vessel"""
    logger.info('Creating new vessel')
    try:
        vessel = vessel_service.create(
            name=request.data.name,
            capacity=request.data.capacity
        )
        logger.info('New vessel created successfully')
        return APIResponse(data=vessel)
    except VesselDuplicatedException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [VesselResponseDuplicated().dict()])
