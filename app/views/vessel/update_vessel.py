from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.vessel import VesselService
from app.schemas.base import APIRequest
from app.schemas.vessel import (
    VesselUpdateRequest,
    VesselResponseNotFound
)
from app.services.exceptions import VesselNotFoundException
from app.views.exceptions import raise_http_exception


def update_vessel(
    vessel_id: int,
    request: APIRequest[VesselUpdateRequest],
    vessel_service: VesselService = Depends()
) -> Response:
    """Endpoint for updating a vessel"""
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        vessel_service.update(
            vessel_id=vessel_id,
            **update_params
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except VesselNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [VesselResponseNotFound().dict()])
