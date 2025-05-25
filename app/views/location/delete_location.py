from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)
from starlette.responses import Response

from app.services.location import LocationService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.location import (
    LocationResponseNotFound
)
from app.services.exceptions import LocationNotFoundException
from app.views.exceptions import raise_http_exception


def delete_location(
    location_id: int,
    location_service: LocationService = Depends()
) -> Response:
    try:
        location_service.delete(location_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except LocationNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [LocationResponseNotFound().dict()])