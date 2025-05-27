import pytest
from app.models.cargo import (
    Cargo,
    CargoStatus,
    CargoType
)
from app.models.client import Client
from app.models.contract import Contract
from app.models.location import Location
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.schemas.constants import (
    TYPE_CARGO_NOT_FOUND,
    TYPE_CONTRACT_NOT_FOUND
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

def create_contract(db_session, price = 50, client_id = 1, location_id = 1):
    contract = Contract(price=price, client_id=client_id, location_id=location_id)
    db_session.add(contract)
    db_session.commit()
    return contract

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

def test_create_cargo_endpoint(
    db_session,
    client,
    fastapi_app
):
    create_location(db_session)
    create_client(db_session)
    contract = create_contract(db_session)
    cargoes = db_session.query(Cargo).all()
    assert len(cargoes) == 0

    response = client.post(
        fastapi_app.url_path_for('create_cargo'),
        json={
            'data': {
                'type': 0,
                'quantity': 50,
                'contract_id': contract.id
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED
    assert response.json()['data']['status'] == 0

    cargoes = db_session.query(Cargo).all()
    assert len(cargoes) == 1

def test_create_contract_endpoint_no_contract(
    db_session,
    client,
    fastapi_app
):
    cargoes = db_session.query(Contract).all()
    assert len(cargoes) == 0

    response = client.post(
        fastapi_app.url_path_for('create_cargo'),
        json={
            'data': {
                'type': 0,
                'quantity': 50,
                'contract_id': 1
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CONTRACT_NOT_FOUND

    cargoes = db_session.query(Cargo).all()
    assert len(cargoes) == 0

def test_get_cargo_endpoint(
    db_session,
    client,
    fastapi_app
):
    cargoes = db_session.query(Cargo).all()
    assert len(cargoes) == 0

    response = client.get(
        fastapi_app.url_path_for('get_cargo', cargo_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CARGO_NOT_FOUND

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    create_cargo(db_session)

    response = client.get(
        fastapi_app.url_path_for('get_cargo', cargo_id=1)
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data']['id'] == 1


def test_list_cargo_endpoint(
    db_session,
    client,
    fastapi_app
):
    cargoes = db_session.query(Cargo).all()
    assert len(cargoes) == 0

    response = client.get(
        fastapi_app.url_path_for('list_cargoes') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data'] == []
    assert response.json()['pagination']['total'] == 0

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    create_cargo(db_session)

    response = client.get(
        fastapi_app.url_path_for('list_cargoes') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == 1
    assert response.json()['pagination']['total'] == 1

    create_cargo(db_session)

    response = client.get(
        fastapi_app.url_path_for('list_cargoes') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == 1
    assert response.json()['pagination']['total'] == 2

def test_delete_cargo_endpoint(
    db_session,
    client,
    fastapi_app
):
    cargoes = db_session.query(Contract).all()
    assert len(cargoes) == 0

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    create_cargo(db_session)

    cargoes = db_session.query(Contract).all()
    assert len(cargoes) == 1

    response = client.delete(
        fastapi_app.url_path_for('delete_cargo', cargo_id=1)
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    cargoes = db_session.query(Cargo).all()
    assert len(cargoes) == 0

    response = client.delete(
        fastapi_app.url_path_for('delete_cargo', cargo_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CARGO_NOT_FOUND

def test_update_cargo_endpoint(
    db_session,
    client,
    fastapi_app
):
    response = client.patch(
        fastapi_app.url_path_for('update_cargo', cargo_id=1),
        json={
            'data': {
                'type': 1
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CARGO_NOT_FOUND

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)
    cargo = create_cargo(db_session, type=CargoType.wood)

    cargo = db_session.query(Cargo).get(1)
    assert cargo.type == CargoType.wood

    response = client.patch(
        fastapi_app.url_path_for('update_cargo', cargo_id=1),
        json={
            'data': {
                'type': 1
            }
        }
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    db_session.refresh(cargo)
    assert cargo.type == CargoType.coal