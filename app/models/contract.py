from typing import List

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Contract(BaseModel):
    """Contract model for database entity"""

    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True)

    price: Mapped[float] = mapped_column(Float)

    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    client: Mapped['Client'] = relationship(back_populates='contracts')

    cargoes: Mapped[List['Cargo']] = relationship(back_populates='contract')

    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'))
    location: Mapped['Location'] = relationship(back_populates='contracts')

    def __str__(self) -> str:
        return (
            f'id={self.id},'
            f'destination={self.location_id},'
            f'price={self.price}'
        )
