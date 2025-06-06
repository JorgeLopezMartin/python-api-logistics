import logging

from fastapi.params import Depends

from app.services.client import ClientService
from app.schemas.base import APIResponsePaginated
from app.schemas.params.client import ClientParams
from app.schemas.client import ClientResponse

logger = logging.getLogger(__name__)

def list_clients(
    params: ClientParams = Depends(),
    client_service: ClientService = Depends()
) -> APIResponsePaginated[ClientResponse]:
    """List existing clients"""
    logger.info('Listing clients')
    page = client_service.list(params)
    return APIResponsePaginated(data=page.data, pagination=page.pagination.__dict__)
