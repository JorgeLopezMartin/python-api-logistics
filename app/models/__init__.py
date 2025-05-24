# Import models here to avoid issues with the SQLAlchemy mapped and Alembic
from app.models.base import BaseModel
from app.models.contract import Contract

# Used by Alembic to track model modifications
metadata = BaseModel.metadata