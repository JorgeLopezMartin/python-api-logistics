import logging

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

logger = logging.getLogger(__name__)


def create_client(
    request: APIRequest[ClientRequest],
    client_service: ClientService = Depends()
) -> APIResponse[ClientResponse]:
    """Endpoint function for creating a new client"""
    logger.info('Creating new client')
    try:
        client = client_service.create(
            name=request.data.name
        )
        logger.info('New client created')
        return APIResponse(data=client)
    except ClientDuplicatedException as ex:
        return raise_http_exception(ex, HTTP_409_CONFLICT, [ClientResponseDuplicated().dict()])
