from fastapi import FastAPI

from app.logging_config import setup_logging
from app.middlewares.db_session import DatabaseSessionMiddleware
from app.views import router

setup_logging()

app = FastAPI()

app.include_router(router)

app.add_middleware(DatabaseSessionMiddleware)
