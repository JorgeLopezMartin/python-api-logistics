from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.cargo import CargoService
from app.schemas.base import APIResponse
from app.schemas.cargo import (
    CargoResponse,
    CargoResponseNotFound
)
from app.services.exceptions import CargoNotFoundException
from app.views.exceptions import raise_http_exception


def get_cargo(
    cargo_id: int,
    cargo_service: CargoService = Depends()
) -> APIResponse[CargoResponse]:
    try:
        cargo = cargo_service.get(id=cargo_id)
        return APIResponse(data=cargo)
    except CargoNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [CargoResponseNotFound().dict()])
