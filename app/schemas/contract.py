from typing import Optional

from pydantic import BaseModel

from app.schemas import constants

class ContractBase(BaseModel):

    class Config:
        from_attributes=True


class ContractRequest(BaseModel):
    """Contract Post request"""

    price: float
    client_id: int
    location_id: int

class ContractResponse(BaseModel):
    """Contract info response"""

    id: int
    price: float
    client_id: int
    location_id: int

class ContractUpdateRequest(BaseModel):
    """Contract PATCH request"""

    price: Optional[float] = None

class ContractResponseDuplicated(BaseModel):
    msg: str = 'Contract - Contract duplicated'
    type: str = constants.TYPE_CONTRACT_DUPLICATED

class ContractResponseNotDeletable(BaseModel):
    msg: str = 'Contract - Contract not deletable'
    type: str = constants.TYPE_CONTRACT_NOT_DELETABLE

class ContractResponseNotFound(BaseModel):
    msg: str = 'Contract - Contract not found'
    type: str = constants.TYPE_CONTRACT_NOT_FOUND
