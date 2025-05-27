import logging

from fastapi.params import Depends

from app.services.location import LocationService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.location import LocationParams
from app.schemas.location import LocationResponse

logger = logging.getLogger(__name__)


def list_locations(
    params: LocationParams = Depends(),
    location_service: LocationService = Depends()
) -> APIResponsePaginated[LocationResponse]:
    """List existing locations"""
    logger.info('Listing locations')
    page = location_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)
