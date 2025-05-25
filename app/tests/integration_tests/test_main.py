import pytest

pytestmark = pytest.mark.integration


def test_ping(client):
    response = client.get('/ping')

    assert response.json() == 'pong'
