from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Track(BaseModel):
    """Database entity to track locations where the cargo has been"""

    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'))
    location: Mapped['Location'] = relationship(back_populates='tracks')

    cargo_id: Mapped[Optional[int]] = mapped_column(ForeignKey('cargoes.id'))
    cargo: Mapped[Optional['Cargo']] = relationship(back_populates='tracks')

    vessel_id: Mapped[int] = mapped_column(ForeignKey('vessels.id'))
    vessel: Mapped['Vessel'] = relationship(back_populates='tracks')

    def __str__(self) -> str:
        return (
            f'id={self.id},'
            f'date={self.date},'
            f'location={self.location_id},'
            f'cargo_id={self.cargo_id},'
            f'vessel_id={self.vessel_id}'
        )