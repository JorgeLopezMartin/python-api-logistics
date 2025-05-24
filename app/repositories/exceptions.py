from sqlalchemy.exc import NoResultFound


class DuplicateException(Exception):
    """Duplicate row in database."""


NotFoundException = NoResultFound
