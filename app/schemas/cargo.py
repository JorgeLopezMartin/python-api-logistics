from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from app.models.cargo import CargoType, CargoStatus
from app.schemas import constants

class CargoBase(BaseModel):

    class Config:
        from_attributes=True

class CargoRequest(BaseModel):
    """Cargo POST request"""

    type: CargoType
    quantity: float
    contract_id: int

class CargoUpdateRequest(BaseModel):
    """Cargo PATCH request"""

    type: Optional[CargoType] = None
    quantity: Optional[float] = None

class CargoResponse(BaseModel):
    """Client info response"""

    id: int
    type: CargoType
    status: CargoStatus
    contract_id: int

class CargoResponseAlreadyDelivered(BaseModel):
    msg: str = 'Cargo - Already delivered'
    type: str = constants.TYPE_CARGO_DELIVERED

class CargoResponseDuplicated(BaseModel):
    msg: str = 'Cargo - Cargo duplicated'
    type: str = constants.TYPE_CARGO_DUPLICATED

class CargoResponseNotDeletable(BaseModel):
    msg: str = 'Cargo - Cargo cannot be deleted'
    type: str = constants.TYPE_CARGO_NOT_DELETABLE

class CargoResponseNotFound(BaseModel):
    msg: str = 'Cargo - Cargo not found'
    type: str = constants.TYPE_CARGO_NOT_FOUND