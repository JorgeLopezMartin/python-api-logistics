from fastapi.params import Depends
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from app.services.client import ClientService
from app.schemas.base import APIRequest
from app.schemas.client import (
    ClientRequest,
    ClientResponseNotFound
)
from app.services.exceptions import ClientNotFoundException
from app.views.exceptions import raise_http_exception


def update_client(
    client_id: int,
    request: APIRequest[ClientRequest],
    client_service: ClientService = Depends()
) -> Response:
    try:
        update_params = {k: v for k, v in vars(request.data).items() if v}
        client_service.update(
            client_id=client_id,
            **update_params
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except ClientNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ClientResponseNotFound().dict()])
