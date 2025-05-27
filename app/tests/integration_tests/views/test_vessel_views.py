import pytest
from app.models.vessel import Vessel
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.schemas.constants import TYPE_VESSEL_NOT_FOUND

pytestmark = pytest.mark.integration

def create_vessel(db_session, name = 'Test', capacity = 50):
    vessel = Vessel(name=name, capacity=50)
    db_session.add(vessel)
    db_session.commit()
    return vessel

def test_create_vessel_endpoint(
    db_session,
    client,
    fastapi_app
):
    vessels = db_session.query(Vessel).all()
    assert len(vessels) == 0

    response = client.post(
        fastapi_app.url_path_for('create_vessel'),
        json={
            'data': {
                'name': 'Test',
                'capacity': 40
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED
    assert response.json()['data']['name'] == 'Test'


def test_get_vessel_endpoint(
    db_session,
    client,
    fastapi_app
):
    vessels = db_session.query(Vessel).all()
    assert len(vessels) == 0

    response = client.get(
        fastapi_app.url_path_for('get_vessel', vessel_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_VESSEL_NOT_FOUND

    create_vessel(db_session, 'Test GET', 50)

    response = client.get(
        fastapi_app.url_path_for('get_vessel', vessel_id=1)
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data']['id'] == 1
    assert response.json()['data']['name'] == 'Test GET'

def test_list_vessel_endpoint(
    db_session,
    client,
    fastapi_app
):
    vessels = db_session.query(Vessel).all()
    assert len(vessels) == 0

    response = client.get(
        fastapi_app.url_path_for('list_vessels') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data'] == []
    assert response.json()['pagination']['total'] == 0

    create_vessel(db_session, 'Test LIST', 50)

    response = client.get(
        fastapi_app.url_path_for('list_vessels') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == 'Test LIST'
    assert response.json()['pagination']['total'] == 1

    create_vessel(db_session, 'Test LIST', 50)

    response = client.get(
        fastapi_app.url_path_for('list_vessels') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == 'Test LIST'
    assert response.json()['pagination']['total'] == 2

def test_delete_vessel_endpoint(
    db_session,
    client,
    fastapi_app
):
    vessels = db_session.query(Vessel).all()
    assert len(vessels) == 0

    create_vessel(db_session, 'Test DELETE', 50)

    vessels = db_session.query(Vessel).all()
    assert len(vessels) == 1

    response = client.delete(
        fastapi_app.url_path_for('delete_vessel', vessel_id=1)
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    vessels = db_session.query(Vessel).all()
    assert len(vessels) == 0

    response = client.delete(
        fastapi_app.url_path_for('delete_vessel', vessel_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_VESSEL_NOT_FOUND

def test_update_vessel_endpoint(
    db_session,
    client,
    fastapi_app
):
    response = client.patch(
        fastapi_app.url_path_for('update_vessel', vessel_id=1),
        json={
            'data': {
                'name': 'UPDATED'
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_VESSEL_NOT_FOUND

    create_vessel(db_session, 'Test UPDATE', 50)

    vessel = db_session.query(Vessel).get(1)
    assert vessel.name == 'Test UPDATE'

    response = client.patch(
        fastapi_app.url_path_for('update_vessel', vessel_id=1),
        json={
            'data': {
                'name': 'UPDATED'
            }
        }
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    db_session.refresh(vessel)
    assert vessel.name == 'UPDATED'
