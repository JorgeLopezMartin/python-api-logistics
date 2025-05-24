from fastapi import FastAPI

from app.middlewares.db_session import DatabaseSessionMiddleware
from app.views import router


app = FastAPI()

app.include_router(router)

app.add_middleware(DatabaseSessionMiddleware)
