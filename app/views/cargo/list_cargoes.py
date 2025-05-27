from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends

from app.services.cargo import CargoService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.cargo import CargoParams
from app.schemas.cargo import CargoResponse

from app.views.exceptions import raise_http_exception


def list_cargoes(
    params: CargoParams = Depends(),
    cargo_service: CargoService = Depends()
) -> APIResponsePaginated[CargoResponse]:
    """List existing cargoes"""

    page = cargo_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)