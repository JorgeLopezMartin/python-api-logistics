import pytest
from app.models.location import Location
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.schemas.constants import TYPE_LOCATION_NOT_FOUND

pytestmark = pytest.mark.integration

def create_location(db_session, name = 'Test', latitude = 123, longitude = 456):
    location = Location(name=name, latitude=latitude, longitude=longitude)
    db_session.add(location)
    db_session.commit()
    return location

def test_create_location_endpoint(
    db_session,
    client,
    fastapi_app
):
    locations = db_session.query(Location).all()
    assert len(locations) == 0

    response = client.post(
        fastapi_app.url_path_for('create_location'),
        json={
            'data': {
                'name': 'Test',
                'latitude': 1234,
                'longitude': 5678
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED
    assert response.json()['data']['name'] == 'Test'

def test_get_location_endpoint(
    db_session,
    client,
    fastapi_app
):
    locations = db_session.query(Location).all()
    assert len(locations) == 0

    response = client.get(
        fastapi_app.url_path_for('get_location', location_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_LOCATION_NOT_FOUND

    create_location(db_session, 'Test GET', 1234, 5678)

    response = client.get(
        fastapi_app.url_path_for('get_location', location_id=1)
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data']['id'] == 1
    assert response.json()['data']['name'] == 'Test GET'

def test_list_location_endpoint(
    db_session,
    client,
    fastapi_app
):
    locations = db_session.query(Location).all()
    assert len(locations) == 0

    response = client.get(
        fastapi_app.url_path_for('list_locations') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data'] == []
    assert response.json()['pagination']['total'] == 0

    create_location(db_session, 'Test LIST', 1234, 5678)

    response = client.get(
        fastapi_app.url_path_for('list_locations') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == 'Test LIST'
    assert response.json()['pagination']['total'] == 1

    create_location(db_session, 'Test LIST', 1234, 5678)

    response = client.get(
        fastapi_app.url_path_for('list_locations') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == 'Test LIST'
    assert response.json()['pagination']['total'] == 2

def test_delete_location_endpoint(
    db_session,
    client,
    fastapi_app
):
    locations = db_session.query(Location).all()
    assert len(locations) == 0

    create_location(db_session, 'Test DELETE', 1234, 5678)

    locations = db_session.query(Location).all()
    assert len(locations) == 1

    response = client.delete(
        fastapi_app.url_path_for('delete_location', location_id=1)
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    locations = db_session.query(Location).all()
    assert len(locations) == 0

    response = client.delete(
        fastapi_app.url_path_for('delete_location', location_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_LOCATION_NOT_FOUND

def test_update_location_endpoint(
    db_session,
    client,
    fastapi_app
):
    response = client.patch(
        fastapi_app.url_path_for('update_location', location_id=1),
        json={
            'data': {
                'name': 'UPDATED'
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_LOCATION_NOT_FOUND

    create_location(db_session, 'Test UPDATE', 1234, 5678)

    location = db_session.query(Location).get(1)
    assert location.name == 'Test UPDATE'

    response = client.patch(
        fastapi_app.url_path_for('update_location', location_id=1),
        json={
            'data': {
                'name': 'UPDATED'
            }
        }
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    db_session.refresh(location)
    assert location.name == 'UPDATED'
