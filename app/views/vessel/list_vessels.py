from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends

from app.services.vessel import VesselService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.vessel import VesselParams
from app.schemas.vessel import VesselResponse

from app.views.exceptions import raise_http_exception


def list_vessels(
    params: VesselParams = Depends(),
    vessel_service: VesselService = Depends()
) -> APIResponsePaginated[VesselResponse]:
    """List existing vessels"""

    page = vessel_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)