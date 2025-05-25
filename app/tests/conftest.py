import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.main import app
from app.models import Location, metadata
from app.settings import get_settings

@pytest.fixture(scope='module')
def client():
    return TestClient(app)

@pytest.fixture(scope='session')
def engine():
    return create_engine(get_settings().SQLALCHEMY_DATABASE_URI)

@pytest.fixture(scope='function')
def tables(engine):
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(engine, tables):
    with engine.connect() as connection:
        session = Session(bind=connection)
        yield session
        session.close()

@pytest.fixture()
def fastapi_app():
    return app