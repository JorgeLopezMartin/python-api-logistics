from typing import List, Optional

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Contract(BaseModel):
    """Contract model for database entity"""

    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True)

    client_name: Mapped[str] = mapped_column(String(100))
    cargo_type: Mapped[str] = mapped_column(String(50))
    destination: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)

    def __str__(self) -> str:
        return (
            f'client_name={self.client_name},'
            f'cargo_type={self.cargo_type},'
            f'destination=¨{self.destination},'
            f'price={self.price}'
        )
