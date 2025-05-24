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