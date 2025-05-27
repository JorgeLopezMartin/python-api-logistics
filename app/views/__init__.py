from fastapi.routing import APIRouter

from app.views import ping
from app.views.cargo import cargoes_router
from app.views.client import clients_router
from app.views.contract import contracts_router
from app.views.location import locations_router
from app.views.vessel import vessels_router


router = APIRouter()

router.include_router(ping.ping_router)
router.include_router(cargoes_router, prefix='/cargo')
router.include_router(clients_router, prefix='/client')
router.include_router(contracts_router, prefix='/contract')
router.include_router(locations_router, prefix='/location')
router.include_router(vessels_router, prefix='/vessel')