from typing import Any, List, Optional

from sqlalchemy import and_, cast, or_
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.sql.elements import ClauseList


class QueryFilter:
    """Complex filter to be used in database queries.

    Once you instantiate the object, you may add as many conditions
    (filters) as required. The 'and' operator is applied to all of
    them.

    The resulting object is a callable that can be passed into your
    SQLAlchemy query::

        >>> db_session: DatabaseSession
        >>> q = QueryFilter()
        >>> db_session.query(MyModel).filter(q()).all()
    """

    def __init__(self, *args: Any) -> None:
        self.filter: ClauseList = and_(True, *args)

    def __call__(self, *args: Any, **kwargs: Any) -> ClauseList:
        """Return SQLAlchemy filter to implement this complex filter."""

        return self.filter

    def between(
            self,
            column: QueryableAttribute,
            low_value: Optional[Any],
            high_value: Optional[Any]
    ) -> None:
        """Column must be between low_value and high_value.

        If no values are given, the filter isn't applied.
        """

        if low_value is not None:
            self.filter &= column >= low_value

        if high_value is not None:
            self.filter &= column <= high_value

    def not_contain(
            self,
            column: QueryableAttribute,
            value: Optional[Any]
    ) -> None:
        """Column values must not contain the given value.

        This filter only makes sense if column is of type ARRAY.

        If no value is given, the filter isn't applied.
        """

        if value:
            # self_group() is required to make ANY take precedence over NOT
            self.filter &= ~(column.any(value).self_group())

    def equal(self, column: QueryableAttribute, value: Optional[Any]) -> None:
        """Column must have the given value.

        If no value is given, the filter isn't applied.
        """

        if value is not None:
            self.strict_equal(column, value)

    def strict_equal(self, column: QueryableAttribute, value: Any) -> None:
        """Column must have the given value."""

        self.filter &= column == value

    def ilike(self, column: QueryableAttribute, value: Optional[Any]) -> None:
        """Column must match with the value.

        If no values are given, the filter isn't applied.
        """

        if value:
            self.filter &= column.ilike(f'%{value}%')

    def in_list(
            self,
            column: QueryableAttribute,
            values: Optional[List[Any]]
    ) -> None:
        """Column must have a value in the list of given values.

        If no values are given, the filter isn't applied.
        """

        if values:
            self.filter &= column.in_(values)

    def overlap(
            self,
            column: QueryableAttribute,
            values: Optional[List[Any]]
    ) -> None:
        """Column values must overlap with the list of given values.

        This filter only makes sense if column is of type ARRAY.

        If no values are given, the filter isn't applied.
        """

        if values:
            self.filter &= column.overlap(cast(values, column.type))

    def any_equal(
            self,
            columns: List[QueryableAttribute],
            value: Optional[Any]
    ) -> None:
        """One or more columns must have the given value.

        If no value is given, the filter isn't applied.
        """

        if value is not None:
            filters = (c == value for c in columns)
            self.filter &= or_(filters)  # type: ignore

    def any_ilike(
            self,
            columns: List[QueryableAttribute],
            value: Optional[Any]
    ) -> None:
        """One or more columns ilike equal.

        If no value is given, the filter isn't applied.
        """

        if value is not None:
            filters = (c.ilike(f'%{value}%') for c in columns)
            self.filter &= or_(filters)  # type: ignore

    def any_in_list(
            self,
            columns: List[QueryableAttribute],
            values: Optional[List[Any]]
    ) -> None:
        """One or more column values match a value from the list.

        If no values are given, the filter isn't applied.
        """

        if values:
            filters = (c.in_(values) for c in columns)
            self.filter &= or_(filters)  # type: ignore
