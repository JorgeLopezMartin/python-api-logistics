from datetime import datetime

import pytest

from app.models import Client, Contract, Location

pytestmark = pytest.mark.integration


def test_contract_creation(db_session):
    location = Location(name='TEST', latitude=1, longitude=2)
    db_session.add(location)
    db_session.commit()

    myclient = Client(name='Test')
    db_session.add(myclient)
    db_session.commit()

    contract = Contract(price=50, client_id=myclient.id, location_id = location.id)
    db_session.add(contract)
    db_session.commit()

    assert contract.client_id == myclient.id
    assert contract.location_id == location.id
    assert isinstance(contract.id, int)
    assert isinstance(contract.created, datetime)
    assert isinstance(contract.modified, datetime)