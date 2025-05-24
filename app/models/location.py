from typing import List, Optional

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Location(BaseModel):
    """Location model for database entity"""

    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    contracts: Mapped[List['Contract']] = relationship(back_populates='location')

    def __str__(self) -> str:
        return (
            f'id={self.id},'
            f'name={self.name},'
            f'latitude={self.latitude},'
            f'longitude={self.longitude}'
        )