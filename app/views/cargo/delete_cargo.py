import logging

from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from starlette.responses import Response

from app.services.cargo import CargoService
from app.schemas.cargo import (
    CargoResponseNotDeletable,
    CargoResponseNotFound
)
from app.services.exceptions import (
    CargoNotDeletableException,
    CargoNotFoundException
)
from app.views.exceptions import raise_http_exception

logger = logging.getLogger(__name__)


def delete_cargo(
    cargo_id: int,
    cargo_service: CargoService = Depends()
) -> Response:
    """Endpoint function for DELETE /cargo/{cargo_id}
    Deletes a cargo from database. Returns OK if successful
    Returns 404 if the cargo cannot be found in DB"""
    logger.info('Deleting cargo %s', cargo_id)
    try:
        cargo_service.delete(cargo_id)
        logger.info('Cargo %s deleted', cargo_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except CargoNotDeletableException as ex:
        logger.info('Cargo %s not deletable', cargo_id)
        return raise_http_exception(ex, HTTP_409_CONFLICT, [CargoResponseNotDeletable().dict()])
    except CargoNotFoundException as ex:
        logger.info('Cargo %s not found', cargo_id)
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [CargoResponseNotFound().dict()])
