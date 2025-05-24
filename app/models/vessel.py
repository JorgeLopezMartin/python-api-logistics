from sqlalchemy import String, Enum, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Vessel(BaseModel):
    """Vessel model for database entity"""

    __tablename__ = 'vessels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[float] = mapped_column(Float)

    def __str__(self) -> str:
        return (
            f'id={self.id},'
            f'name={self.name},'
            f'capacity={self.capacity}'
        )
