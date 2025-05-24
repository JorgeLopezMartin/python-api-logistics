from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

from app.database.session import DatabaseSession


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    """Add a database session to the current request."""

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint
    ) -> Response:

        try:
            request.state.db_session = DatabaseSession()
            response = await call_next(request)

        finally:
            request.state.db_session.close()

        return response
