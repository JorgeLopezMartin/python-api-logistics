from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.location import LocationService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.location import (
    LocationUpdateRequest,
    LocationResponse,
    LocationResponseNotFound
)
from app.services.exceptions import LocationNotFoundException
from app.views.exceptions import raise_http_exception


def update_location(
    location_id: int,
    request: APIRequest[LocationUpdateRequest],
    location_service: LocationService = Depends()
) -> Response:
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        location = location_service.update(
            location_id=location_id,
            **update_params
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except LocationNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [LocationResponseNotFound().dict()])
