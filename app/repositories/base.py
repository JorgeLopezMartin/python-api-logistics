from types import TracebackType
from typing import Any, Optional, Type

from fastapi import Depends
from psycopg2.errors import \
    UniqueViolation  # pylint: disable=no-name-in-module
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.query import PaginatedQuery
from app.database.session import get_db
from app.models.base import BaseModel
from app.repositories.exceptions import DuplicateException


class BaseRepository:
    """Base class for model repositories."""

    db_session: Session

    def __init__(self, db_session: Session = Depends(get_db)) -> None:
        self.db_session = db_session

    def __enter__(self) -> 'BaseRepository':
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> None:
        if exc_type:
            self._rollback()

        else:
            self._commit()

    def get(self, entity_class: Type[BaseModel], **filters: Any) -> BaseModel:
        """Find entity given some filter criteria.

        :raises `NotFoundException`: Entity not found.
        """

        return self.query(entity_class).filter_by(**filters).one()

    def delete(self, instance: BaseModel) -> BaseModel:
        """Delete a specific entity."""

        return self.db_session.delete(instance)

    def patch(self, entity: BaseModel, **fields: Any) -> BaseModel:
        """Update a model with the given fields."""

        for field, value in fields.items():
            setattr(entity, field, value)

        self.persist(entity)

        return entity

    def persist(self, *instances: BaseModel) -> None:
        """Persist multiple instances."""

        self.db_session.add_all(instances)

    def query(self, entity_class: Type[BaseModel]) -> PaginatedQuery:
        """Return a query with pagination support."""

        return PaginatedQuery(self.db_session, entity_class)

    def row_count(self, entity_class: Type[BaseModel], **filters: Any) -> int:
        """Get number of rows that match given filter criteria."""

        return self.db_session.query(entity_class).filter_by(**filters).count()

    def _commit(self) -> None:
        """Commit database session.

        If an exception is triggered, handle it appropriately.

        :raises `DuplicateException`: Duplicate row in database.
        :raises `IntegrityError`: Integrity issue in database.
        """

        try:
            self.db_session.commit()

        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise DuplicateException() from e

            raise e

    def _rollback(self) -> None:
        """Rollback database session."""

        self.db_session.rollback()
