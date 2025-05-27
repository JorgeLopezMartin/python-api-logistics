import logging

from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.cargo import CargoService
from app.schemas.base import APIRequest
from app.schemas.cargo import (
    CargoUpdateRequest,
    CargoResponseNotFound
)
from app.services.exceptions import CargoNotFoundException
from app.views.exceptions import raise_http_exception


logger = logging.getLogger(__name__)

def update_cargo(
    cargo_id: int,
    request: APIRequest[CargoUpdateRequest],
    cargo_service: CargoService = Depends()
) -> Response:
    """Endpoint function for updating a specific cargo."""
    logger.info('Updating cargo %s', cargo_id)
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        cargo_service.update(
            cargo_id=cargo_id,
            **update_params
        )
        logger.info('Cargo %s updated', cargo_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except CargoNotFoundException as ex:
        logger.info('Cargo %s not found', cargo_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [CargoResponseNotFound().dict()])
