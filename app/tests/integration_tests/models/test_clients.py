from datetime import datetime

import pytest

from app.models import Client

pytestmark = pytest.mark.integration


def test_client_creation(db_session):
    myclient = Client(name='Test')
    db_session.add(myclient)
    db_session.commit()

    assert myclient.name == 'Test'
    assert isinstance(myclient.id, int)
    assert isinstance(myclient.created, datetime)
    assert isinstance(myclient.modified, datetime)