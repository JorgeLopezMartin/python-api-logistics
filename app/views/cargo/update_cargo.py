from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.cargo import CargoService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.cargo import (
    CargoUpdateRequest,
    CargoResponse,
    CargoResponseNotFound
)
from app.services.exceptions import CargoNotFoundException
from app.views.exceptions import raise_http_exception


def update_cargo(
    cargo_id: int,
    request: APIRequest[CargoUpdateRequest],
    cargo_service: CargoService = Depends()
) -> Response:
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        cargo = cargo_service.update(
            cargo_id=cargo_id,
            **update_params
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except CargoNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [CargoResponseNotFound().dict()])
