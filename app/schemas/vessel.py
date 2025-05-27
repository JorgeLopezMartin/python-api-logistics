from typing import Optional

from pydantic import BaseModel

from app.schemas import constants

class VesselBase(BaseModel):

    class Config:
        from_attributes=True


class VesselRequest(BaseModel):
    """Vessel Post request"""

    name: str
    capacity: float

class VesselResponse(BaseModel):
    """Vessel info response"""

    id: int
    name: str
    capacity: float

class VesselUpdateRequest(BaseModel):
    """Vessel PATCH request"""

    name: Optional[str] = None
    capacity: Optional[float] = None

class VesselResponseNotDeletable(BaseModel):
    msg: str = 'Vessel - Vessel not deletable'
    type: str = constants.TYPE_VESSEL_NOT_DELETABLE

class VesselResponseDuplicated(BaseModel):
    msg: str = 'Vessel - Vessel duplicated'
    type: str = constants.TYPE_VESSEL_DUPLICATED

class VesselResponseNotFound(BaseModel):
    msg: str = 'Vessel - Vessel not found'
    type: str = constants.TYPE_VESSEL_NOT_FOUND
