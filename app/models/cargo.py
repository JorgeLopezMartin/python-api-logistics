import enum
from typing import List, Optional

from sqlalchemy import String, Enum, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class CargoType(enum.Enum):
    wood = 0
    coal = 1
    uranium = 2

class CargoStatus(enum.Enum):
    pending = 0
    in_transit = 1
    delivered = 2

class Cargo(BaseModel):
    """Cargo model for database entity"""

    __tablename__ = 'cargoes'

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[CargoType] = mapped_column(Enum(CargoType))
    quantity: Mapped[int] = mapped_column(Float)
    status: Mapped[CargoStatus] = mapped_column(Enum(CargoStatus))

    contract_id: Mapped[int] = mapped_column(ForeignKey('contracts.id'))
    contract: Mapped['Contract'] = relationship(back_populates='cargoes')

    tracks: Mapped[List['Track']] = relationship(back_populates='cargo')

    def __str__(self) -> str:
        return (
            f'id={self.id},'
            f'type={self.type},'
            f'quantity={self.quantity},'
            f'status={self.status}'
        )