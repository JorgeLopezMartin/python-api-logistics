from datetime import datetime

import pytest

from app.models import (
    Cargo,
    Client,
    Contract,
    Location,
    Track,
    Vessel
)
from app.models.cargo import CargoStatus, CargoType

pytestmark = pytest.mark.integration


def test_track_creation(db_session):
    location = Location(name='TEST', latitude=1, longitude=2)
    db_session.add(location)
    db_session.commit()

    myclient = Client(name='Test')
    db_session.add(myclient)
    db_session.commit()

    contract = Contract(price=50, client_id=myclient.id, location_id = location.id)
    db_session.add(contract)
    db_session.commit()

    cargo = Cargo(type=CargoType.wood, quantity=50, status=CargoStatus.pending, contract_id=1)
    db_session.add(cargo)
    db_session.commit()

    vessel = Vessel(name='TEST', capacity=50)
    db_session.add(vessel)
    db_session.commit()

    track = Track(
        date="2025-05-25T18:30:00",
        location_id=location.id,
        cargo_id=cargo.id,
        vessel_id=vessel.id
    )
    db_session.add(track)
    db_session.commit()

    assert track.location_id == location.id
    assert isinstance(track.id, int)
    assert isinstance(track.created, datetime)
    assert isinstance(track.modified, datetime)