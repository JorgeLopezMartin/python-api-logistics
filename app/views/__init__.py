from fastapi.routing import APIRouter

from app.views import ping
from app.views.client import clients_router
from app.views.location import locations_router


router = APIRouter()

router.include_router(ping.ping_router)
router.include_router(clients_router, prefix='/client')
router.include_router(locations_router, prefix='/location')