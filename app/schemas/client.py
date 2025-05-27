from pydantic import BaseModel

from app.schemas import constants

class ClientBase(BaseModel):

    class Config:
        from_attributes=True

class ClientRequest(BaseModel):
    """Client POST request"""

    name: str

class ClientResponse(BaseModel):
    """Client info response"""

    id: int
    name: str

class ClientResponseDuplicated(BaseModel):
    msg: str = 'Client - Client duplicated'
    type: str = constants.TYPE_CLIENT_DUPLICATED

class ClientResponseNotDeletable(BaseModel):
    msg: str = 'Client - Client cannot be deleted'
    type: str = constants.TYPE_CLIENT_NOT_DELETABLE

class ClientResponseNotFound(BaseModel):
    msg: str = 'Client - Client not found'
    type: str = constants.TYPE_CLIENT_NOT_FOUND
