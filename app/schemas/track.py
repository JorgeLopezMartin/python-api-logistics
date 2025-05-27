from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import constants

class TrackBase(BaseModel):

    class Config:
        from_attributes=True


class TrackRequest(BaseModel):
    """Track Post request"""

    date: datetime
    location_id: int
    cargo_id: Optional[int] = None
    vessel_id: int

class TrackResponse(BaseModel):
    """Track info response"""

    id: int
    date: datetime
    location_id: int
    cargo_id: Optional[int]
    vessel_id: int

class TrackUpdateRequest(BaseModel):
    """Track PATCH request"""

    date: datetime

class TrackResponseDuplicated(BaseModel):
    msg: str = 'Track - Track duplicated'
    type: str = constants.TYPE_TRACK_DUPLICATED

class TrackResponseNotDeletable(BaseModel):
    msg: str = 'Track - Track not deletable'
    type: str = constants.TYPE_TRACK_NOT_DELETABLE

class TrackResponseNotFound(BaseModel):
    msg: str = 'Track - Track not found'
    type: str = constants.TYPE_TRACK_NOT_FOUND
