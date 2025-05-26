import pytest
from app.models.client import Client
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

from app.schemas.constants import TYPE_CLIENT_NOT_FOUND

pytestmark = pytest.mark.integration

def create_client(db_session, name = 'Test'):
    client = Client(name=name)
    db_session.add(client)
    db_session.commit()
    return client

def test_create_client_endpoint(
    db_session,
    client,
    fastapi_app
):
    clients = db_session.query(Client).all()
    assert len(clients) == 0

    response = client.post(
        fastapi_app.url_path_for('create_client'),
        json={
            'data': {
                'name': 'Test'
            }
        }
    )

    assert response.status_code == HTTP_201_CREATED
    assert response.json()['data']['name'] == 'Test'

def test_get_client_endpoint(
    db_session,
    client,
    fastapi_app
):
    clients = db_session.query(Client).all()
    assert len(clients) == 0

    response = client.get(
        fastapi_app.url_path_for('get_client', client_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CLIENT_NOT_FOUND

    create_client(db_session, 'Test GET')

    response = client.get(
        fastapi_app.url_path_for('get_client', client_id=1)
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data']['id'] == 1
    assert response.json()['data']['name'] == 'Test GET'

def test_list_client_endpoint(
    db_session,
    client,
    fastapi_app
):
    clients = db_session.query(Client).all()
    assert len(clients) == 0

    response = client.get(
        fastapi_app.url_path_for('list_clients') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()['data'] == []
    assert response.json()['pagination']['total'] == 0

    create_client(db_session, 'Test LIST')

    response = client.get(
        fastapi_app.url_path_for('list_clients') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == 'Test LIST'
    assert response.json()['pagination']['total'] == 1

    create_client(db_session, 'Test LIST')

    response = client.get(
        fastapi_app.url_path_for('list_clients') + '?page=1&page_size=1'
    )

    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['name'] == 'Test LIST'
    assert response.json()['pagination']['total'] == 2

def test_delete_client_endpoint(
    db_session,
    client,
    fastapi_app
):
    clients = db_session.query(Client).all()
    assert len(clients) == 0

    create_client(db_session, 'Test DELETE')

    clients = db_session.query(Client).all()
    assert len(clients) == 1

    response = client.delete(
        fastapi_app.url_path_for('delete_client', client_id=1)
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    clients = db_session.query(Client).all()
    assert len(clients) == 0

    response = client.delete(
        fastapi_app.url_path_for('delete_client', client_id=1)
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CLIENT_NOT_FOUND

def test_update_client_endpoint(
    db_session,
    client,
    fastapi_app
):
    response = client.patch(
        fastapi_app.url_path_for('update_client', client_id=1),
        json={
            'data': {
                'name': 'UPDATED'
            }
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'][0]['type'] == TYPE_CLIENT_NOT_FOUND

    create_client(db_session, 'Test UPDATE')

    myclient = db_session.query(Client).get(1)
    assert myclient.name == 'Test UPDATE'

    response = client.patch(
        fastapi_app.url_path_for('update_client', client_id=1),
        json={
            'data': {
                'name': 'UPDATED'
            }
        }
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    db_session.refresh(myclient)
    assert myclient.name == 'UPDATED'
