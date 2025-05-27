from datetime import datetime

import pytest

from app.models import Vessel

pytestmark = pytest.mark.integration


def test_vessel_creation(db_session):
    vessel = Vessel(name='TEST', capacity=50)
    db_session.add(vessel)
    db_session.commit()

    assert vessel.name == 'TEST'
    assert isinstance(vessel.id, int)
    assert isinstance(vessel.created, datetime)
    assert isinstance(vessel.modified, datetime)