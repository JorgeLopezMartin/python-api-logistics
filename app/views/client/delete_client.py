from fastapi.params import Depends
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from starlette.responses import Response

from app.services.client import ClientService
from app.schemas.client import (
    ClientResponseNotDeletable,
    ClientResponseNotFound
)
from app.services.exceptions import (
    ClientNotDeletableException,
    ClientNotFoundException
)
from app.views.exceptions import raise_http_exception


def delete_client(
    client_id: int,
    client_service: ClientService = Depends()
) -> Response:
    try:
        client_service.delete(client_id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except ClientNotDeletableException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [ClientResponseNotDeletable().dict()])
    except ClientNotFoundException as ex:
        return raise_http_exception(ex, HTTP_404_NOT_FOUND, [ClientResponseNotFound().dict()])
