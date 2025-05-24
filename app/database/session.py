from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm.session import sessionmaker
from starlette.requests import Request

from app.settings import get_settings

engine = create_engine(
    get_settings().SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True
)
DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DatabaseScopedSession = scoped_session(DatabaseSession)


def get_db(request: Request) -> Session:
    return request.state.db_session