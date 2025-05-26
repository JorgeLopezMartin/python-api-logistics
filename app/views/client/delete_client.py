from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)
from starlette.responses import Response

from app.services.client import ClientService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.client import (
    ClientResponseNotFound
)
from app.services.exceptions import ClientNotFoundException
from app.views.exceptions import raise_http_exception


def delete_client(
    client_id: int,
    client_service: ClientService = Depends()
) -> Response:
    try:
        client_service.delete(client_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except ClientNotFoundException as ex:
        raise_http_exception(ex, HTTP_404_NOT_FOUND, [ClientResponseNotFound().dict()])