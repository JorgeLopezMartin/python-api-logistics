import logging

from fastapi.params import Depends

from app.services.cargo import CargoService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.cargo import CargoParams
from app.schemas.cargo import CargoResponse

logger = logging.getLogger(__name__)

def list_cargoes(
    params: CargoParams = Depends(),
    cargo_service: CargoService = Depends()
) -> APIResponsePaginated[CargoResponse]:
    """Endpoint function for listing cargoes.
    List existing cargoes"""
    logger.info('Listing cargoes')
    page = cargo_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)
