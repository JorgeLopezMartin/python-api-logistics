from sqlalchemy.exc import NoResultFound

class DeleteException(Exception):
    """Delete operation causes a db integrity problem"""

class DuplicateException(Exception):
    """Duplicate row in database."""

NotFoundException = NoResultFound
