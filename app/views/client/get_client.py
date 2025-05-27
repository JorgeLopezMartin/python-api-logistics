from fastapi.params import Depends
from starlette.status import (
    HTTP_404_NOT_FOUND
)

from app.services.client import ClientService
from app.schemas.base import APIResponse
from app.schemas.client import (
    ClientResponse,
    ClientResponseNotFound
)
from app.services.exceptions import ClientNotFoundException
from app.views.exceptions import raise_http_exception


def get_client(
    client_id: int,
    client_service: ClientService = Depends()
) -> APIResponse[ClientResponse]:
    """Endpoint function for retrieving a client by ID"""
    try:
        client = client_service.get(id=client_id)
        return APIResponse(data=client)
    except ClientNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ClientResponseNotFound().dict()])
