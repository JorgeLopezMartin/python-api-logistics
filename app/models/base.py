from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

class Base:
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self})'

BaseModel = declarative_base(cls=Base)
