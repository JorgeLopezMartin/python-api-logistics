from fastapi.exceptions import HTTPException


def raise_http_exception(ex, status_code, detail):
    raise HTTPException(
        status_code=status_code,
        detail=detail
    ) from ex
