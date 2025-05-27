import pytest
from app.models.client import Client
from app.models.contract import Contract
from app.models.location import Location
from app.models.cargo import (
    Cargo,
    CargoStatus,
    CargoType
)
from app.models.vessel import Vessel
from app.models.track import Track
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.schemas.constants import (
    TYPE_VESSEL_NOT_FOUND,
    TYPE_LOCATION_NOT_FOUND,
    TYPE_TRACK_NOT_FOUND
)

pytestmark = pytest.mark.integration

def create_client(db_session, name = 'Test'):
    client = Client(name=name)
    db_session.add(client)
    db_session.commit()
    return client

def create_location(db_session, name = 'Test', latitude = 123, longitude = 456):
    location = Location(name=name, latitude=latitude, longitude=longitude)
    db_session.add(location)
    db_session.commit()
    return location

def create_cargo(
    db_session,
    type = CargoType.wood,
    quantity = 50,
    status = CargoStatus.pending,
    contract_id = 1
):
    cargo = Cargo(type=type, quantity=quantity, status=status, contract_id=contract_id)
    db_session.add(cargo)
    db_session.commit()
    return cargo

def create_contract(db_session, price = 50, client_id = 1, location_id = 1):
    contract = Contract(price=price, client_id=client_id, location_id=location_id)
    db_session.add(contract)
    db_session.commit()
    return contract

def create_vessel(db_session, name = 'Test', capacity = 50):
    vessel = Vessel(name=name, capacity=50)
    db_session.add(vessel)
    db_session.commit()
    return vessel

def create_track(
    db_session,
    date = "2025-05-25T18:30:00",
    location_id = 1,
    cargo_id = 1,
    vessel_id = 1
):
    track = Track(date=date, location_id=location_id, cargo_id=cargo_id, vessel_id=vessel_id)
    db_session.add(track)
    db_session.commit()
    return track

def test_create_track_endpoint(
    db_session,
    client,
    fastapi_app
):
    destination = create_location(db_session)
    middle_location = create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    cargo = create_cargo(db_session)
    vessel = create_vessel(db_session)

    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

    cargo = db_session.query(Cargo).get(1)
    assert cargo.status == CargoStatus.pending

    response = client.post(
        fastapi_app.url_path_for('create_track'),
        json={
            'data': {
                'date': "2025-05-25T18:30:00",
                'location_id': middle_location.id,
                'cargo_id': cargo.id,
                'vessel_id': vessel.id
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED

    db_session.refresh(cargo)
    assert cargo.status == CargoStatus.in_transit

    response = client.post(
        fastapi_app.url_path_for('create_track'),
        json={
            'data': {
                'date': "2025-05-25T18:30:00",
                'location_id': destination.id,
                'cargo_id': cargo.id,
                'vessel_id': vessel.id
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED

    db_session.refresh(cargo)
    assert cargo.status == CargoStatus.delivered


def test_create_track_endpoint_empty_cargo(
    db_session,
    client,
    fastapi_app
):
    destination = create_location(db_session)
    middle_location = create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    vessel = create_vessel(db_session)

    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

    response = client.post(
        fastapi_app.url_path_for('create_track'),
        json={
            'data': {
                'date': "2025-05-25T18:30:00",
                'location_id': middle_location.id,
                'vessel_id': vessel.id
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED


def test_create_track_endpoint_no_location(
    db_session,
    client,
    fastapi_app
):
    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    cargo = create_cargo(db_session)
    vessel = create_vessel(db_session)
    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

    response = client.post(
        fastapi_app.url_path_for('create_track'),
        json={
            'data': {
                'date': "2025-05-25T18:30:00",
                'location_id': 100,
                'cargo_id': cargo.id,
                'vessel_id': vessel.id
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_LOCATION_NOT_FOUND

    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

def test_create_track_endpoint_no_vessel(
    db_session,
    client,
    fastapi_app
):
    destination = create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    cargo = create_cargo(db_session)
    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

    response = client.post(
        fastapi_app.url_path_for('create_track'),
        json={
            'data': {
                'date': "2025-05-25T18:30:00",
                'location_id': destination.id,
                'cargo_id': cargo.id,
                'vessel_id': 1
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_VESSEL_NOT_FOUND

    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

def test_list_track_endpoint(
    db_session,
    client,
    fastapi_app
):
    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

    response = client.get(
        fastapi_app.url_path_for('list_tracks') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data'] == []
    assert response.json()['pagination']['total'] == 0

    create_location(db_session)
    middle_location = create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    create_cargo(db_session)
    create_vessel(db_session)
    create_track(db_session, location_id=middle_location.id)

    response = client.get(
        fastapi_app.url_path_for('list_tracks') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == 1
    assert response.json()['pagination']['total'] == 1

    create_track(db_session, location_id=middle_location.id)

    response = client.get(
        fastapi_app.url_path_for('list_tracks') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == 1
    assert response.json()['pagination']['total'] == 2


def test_delete_track_endpoint(
    db_session,
    client,
    fastapi_app
):
    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    create_cargo(db_session)
    create_vessel(db_session)
    create_track(db_session)

    tracks = db_session.query(Track).all()
    assert len(tracks) == 1

    response = client.delete(
        fastapi_app.url_path_for('delete_track', track_id=1)
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    tracks = db_session.query(Track).all()
    assert len(tracks) == 0

    response = client.delete(
        fastapi_app.url_path_for('delete_track', track_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_TRACK_NOT_FOUND

def test_update_track_endpoint(
    db_session,
    client,
    fastapi_app
):
    response = client.patch(
        fastapi_app.url_path_for('update_track', track_id=1),
        json={
            'data': {
                "date": "2026-05-25T18:30:00"
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_TRACK_NOT_FOUND

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    create_cargo(db_session)
    create_vessel(db_session)
    create_track(db_session)

    track = db_session.query(Track).get(1)
    assert str(track.date) == "2025-05-25 18:30:00+00:00"

    response = client.patch(
        fastapi_app.url_path_for('update_track', track_id=1),
        json={
            'data': {
                "date": "2026-05-25T18:30:00"
            }
        }
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    db_session.refresh(track)
    assert str(track.date) == "2026-05-25 18:30:00+00:00"
