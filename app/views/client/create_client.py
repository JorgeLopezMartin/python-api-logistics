from fastapi.params import Depends
from starlette.status import (
    HTTP_409_CONFLICT
)

from app.services.client import ClientService
from app.schemas.base import APIRequest, APIResponse
from app.schemas.client import (
    ClientRequest,
    ClientResponse,
    ClientResponseDuplicated
)
from app.services.exceptions import ClientDuplicatedException
from app.views.exceptions import raise_http_exception


def create_client(
    request: APIRequest[ClientRequest],
    client_service: ClientService = Depends()
) -> APIResponse[ClientResponse]:
    try:
        client = client_service.create(
            name=request.data.name
        )
        return APIResponse(data=client)
    except ClientDuplicatedException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [ClientResponseDuplicated().dict()])
