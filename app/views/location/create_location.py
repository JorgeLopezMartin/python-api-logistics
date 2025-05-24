from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_409_CONFLICT
)

from app.services.location import LocationService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.location import (
    LocationRequest,
    LocationResponse,
)
from app.services.exceptions import LocationDuplicatedException



def create_location(
    request: APIRequest[LocationRequest],
    location_service: LocationService = Depends()
) -> APIResponse[LocationResponse]:
    try:
        location = location_service.create(
            name=request.data.name,
            latitude=request.data.latitude,
            longitude=request.data.longitude
        )
        return APIResponse(data=location)
    except LocationDuplicatedException as ex:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=[ex]
        )