from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)
from starlette.responses import Response

from app.services.vessel import VesselService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.vessel import (
    VesselResponseNotFound
)
from app.services.exceptions import VesselNotFoundException
from app.views.exceptions import raise_http_exception


def delete_vessel(
    vessel_id: int,
    vessel_service: VesselService = Depends()
) -> Response:
    try:
        vessel_service.delete(vessel_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except VesselNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [VesselResponseNotFound().dict()])