from typing import List, Optional

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Client(BaseModel):
    """Client model for database entity"""

    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))
    contracts: Mapped[List['Contract']] = relationship(back_populates='client')

    def __str__(self) -> str:
        return (
            f'id={self.id},'
            f'name={self.name}'
        )