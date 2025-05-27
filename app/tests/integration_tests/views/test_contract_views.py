import pytest
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
    TYPE_CLIENT_NOT_FOUND,
    TYPE_CONTRACT_NOT_FOUND,
    TYPE_LOCATION_NOT_FOUND
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

def test_create_contract_endpoint(
    db_session,
    client,
    fastapi_app
):
    location = create_location(db_session)
    myclient = create_client(db_session)
    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

    response = client.post(
        fastapi_app.url_path_for('create_contract'),
        json={
            'data': {
                'price': 40,
                'client_id': myclient.id,
                'location_id': location.id
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED

    contracts = db_session.query(Contract).all()
    assert len(contracts) == 1

def test_create_contract_endpoint_no_client(
    db_session,
    client,
    fastapi_app
):
    location = create_location(db_session)
    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

    response = client.post(
        fastapi_app.url_path_for('create_contract'),
        json={
            'data': {
                'price': 40,
                'client_id': 1,
                'location_id': location.id
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CLIENT_NOT_FOUND

    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

def test_create_contract_endpoint_no_location(
    db_session,
    client,
    fastapi_app
):
    myclient = create_client(db_session)
    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

    response = client.post(
        fastapi_app.url_path_for('create_contract'),
        json={
            'data': {
                'price': 40,
                'client_id': myclient.id,
                'location_id': 1
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_LOCATION_NOT_FOUND

    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

def test_get_contract_endpoint(
    db_session,
    client,
    fastapi_app
):
    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

    response = client.get(
        fastapi_app.url_path_for('get_contract', contract_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CONTRACT_NOT_FOUND

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)

    response = client.get(
        fastapi_app.url_path_for('get_contract', contract_id=1)
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data']['id'] == 1


def test_list_contract_endpoint(
    db_session,
    client,
    fastapi_app
):
    contracts = db_session.query(Location).all()
    assert len(contracts) == 0

    response = client.get(
        fastapi_app.url_path_for('list_contracts') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data'] == []
    assert response.json()['pagination']['total'] == 0

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)

    response = client.get(
        fastapi_app.url_path_for('list_contracts') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == 1
    assert response.json()['pagination']['total'] == 1

    create_contract(db_session)

    response = client.get(
        fastapi_app.url_path_for('list_contracts') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == 1
    assert response.json()['pagination']['total'] == 2

def test_delete_contract_endpoint(
    db_session,
    client,
    fastapi_app
):
    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

    create_location(db_session)
    create_client(db_session)
    create_contract(db_session)

    contracts = db_session.query(Contract).all()
    assert len(contracts) == 1

    response = client.delete(
        fastapi_app.url_path_for('delete_contract', contract_id=1)
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    contracts = db_session.query(Contract).all()
    assert len(contracts) == 0

    response = client.delete(
        fastapi_app.url_path_for('delete_contract', contract_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CONTRACT_NOT_FOUND

def test_update_contract_endpoint(
    db_session,
    client,
    fastapi_app
):
    response = client.patch(
        fastapi_app.url_path_for('update_contract', contract_id=1),
        json={
            'data': {
                'price': 10.5
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CONTRACT_NOT_FOUND

    location = create_location(db_session)
    myclient = create_client(db_session)
    create_contract(db_session, price=5, client_id=myclient.id, location_id=location.id)

    contract = db_session.query(Contract).get(1)
    assert contract.price == 5.0

    response = client.patch(
        fastapi_app.url_path_for('update_contract', contract_id=1),
        json={
            'data': {
                'price': 10.5
            }
        }
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    db_session.refresh(contract)
    assert contract.price == 10.5