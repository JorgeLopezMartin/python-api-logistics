# Import models here to avoid issues with the SQLAlchemy mapped and Alembic
from app.models.base import BaseModel
from app.models.cargo import Cargo
from app.models.client import Client
from app.models.contract import Contract
from app.models.location import Location
from app.models.track import Track
from app.models.vessel import Vessel

# Used by Alembic to track model modifications
metadata = BaseModel.metadata