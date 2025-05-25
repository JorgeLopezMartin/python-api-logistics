from datetime import datetime

import pytest

from app.models import Location

pytestmark = pytest.mark.integration


def test_location_creation(db_session):
    location = Location(name='TEST', latitude=1, longitude=2)
    db_session.add(location)
    db_session.commit()

    assert location.name == 'TEST'
    assert isinstance(location.id, int)
    assert isinstance(location.created, datetime)
    assert isinstance(location.modified, datetime)