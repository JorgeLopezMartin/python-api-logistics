from typing import Generic, List, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class APIErrorResponse(GenericModel, Generic[DataT]):
    """API error response schema.

    Error models are given in the **detail** field.
    """

    detail: List[DataT]


class APIRequest(GenericModel, Generic[DataT]):
    """API request schema.

    The corresponding resources are given within the **data** field.
    """

    data: DataT


class APIResponse(GenericModel, Generic[DataT]):
    """API response schema.

    The corresponding resources are given within the **data** field.
    """

    data: DataT

class Pagination(BaseModel):
    """Pagination field"""

    page: int
    page_size: int
    total: int

    class Config:
        orm_mode: True

class APIResponsePaginated(GenericModel, Generic[DataT]):
    """API schema for paginated responses"""

    data: List[DataT]
    pagination: Pagination

    class Config:
        orm_mode: True