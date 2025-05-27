from datetime import datetime

import pytest

from app.models import (
    Cargo,
    Client,
    Contract,
    Location
)
from app.models.cargo import CargoStatus, CargoType

pytestmark = pytest.mark.integration


def test_cargo_creation(db_session):
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

    assert cargo.contract_id == contract.id
    assert isinstance(cargo.id, int)
    assert isinstance(cargo.created, datetime)
    assert isinstance(cargo.modified, datetime)