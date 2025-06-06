from typing import Optional

from pydantic import BaseModel

from app.schemas import constants

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

class LocationUpdateRequest(BaseModel):
    """Location PATCH request"""

    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class LocationResponseNotDeletable(BaseModel):
    msg: str = 'Location - Location not deletable'
    type: str = constants.TYPE_LOCATION_NOT_DELETABLE

class LocationResponseDuplicated(BaseModel):
    msg: str = 'Location - Location duplicated'
    type: str = constants.TYPE_LOCATION_DUPLICATED

class LocationResponseNotFound(BaseModel):
    msg: str = 'Location - Location not found'
    type: str = constants.TYPE_LOCATION_NOT_FOUND
