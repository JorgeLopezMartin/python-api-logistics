from fastapi.routing import APIRouter

ping_router = APIRouter()


@ping_router.get('/ping')
def ping() -> str:
    return 'pong'
