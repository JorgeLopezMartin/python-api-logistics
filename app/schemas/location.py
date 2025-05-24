from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field

class LocationBase(BaseModel):

    class Config:
        from_attributes=True


class LocationRequest(BaseModel):
    """Location Post request"""

    name: str
    latitude: float
    longitude: float

class LocationResponse(BaseModel):
    """Location info response"""

    id: int
    name: str
    latitude: float
    longitude: float