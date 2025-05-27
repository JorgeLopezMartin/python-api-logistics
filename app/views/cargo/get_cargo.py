import logging

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

logger = logging.getLogger(__name__)

def get_cargo(
    cargo_id: int,
    cargo_service: CargoService = Depends()
) -> APIResponse[CargoResponse]:
    """Endpoint function for GET /cargo/{cargo_id}
    Finds cargo from DB by ID.
    Returns 404 if not found in DB.
    """
    logger.info('Retrieving cargo %s', cargo_id)
    try:
        cargo = cargo_service.get(id=cargo_id)
        logger.info('Cargo %s found', cargo_id)
        return APIResponse(data=cargo)
    except CargoNotFoundException as ex:
        logger.info('Cargo %s not found', cargo_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [CargoResponseNotFound().dict()])
