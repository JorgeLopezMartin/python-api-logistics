from fastapi.params import Depends

from app.services.location import LocationService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.location import LocationParams
from app.schemas.location import LocationResponse


def list_locations(
    params: LocationParams = Depends(),
    location_service: LocationService = Depends()
) -> APIResponsePaginated[LocationResponse]:
    """List existing locations"""

    page = location_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)
