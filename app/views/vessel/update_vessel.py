from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.vessel import VesselService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.vessel import (
    VesselUpdateRequest,
    VesselResponse,
    VesselResponseNotFound
)
from app.services.exceptions import VesselNotFoundException
from app.views.exceptions import raise_http_exception


def update_vessel(
    vessel_id: int,
    request: APIRequest[VesselUpdateRequest],
    vessel_service: VesselService = Depends()
) -> Response:
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        vessel = vessel_service.update(
            vessel_id=vessel_id,
            **update_params
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except VesselNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [VesselResponseNotFound().dict()])
