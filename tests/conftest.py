from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
import os
from fastapi.testclient import TestClient

from src.config import settings
from src.main import app
from src.database import Base, get_session

SQLALCHEMY_DATABASE_URI_TEST = f'postgresql://{settings.DATABASE_USER_TEST}:{settings.DATABASE_PASSWORD_TEST}@{settings.DATABASE_HOST_TEST}:{settings.DATABASE_PORT_TEST}/{settings.DATABASE_NAME_TEST}'

engine = create_engine(SQLALCHEMY_DATABASE_URI_TEST)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='session')
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def overrider_get_session():
    try:
        session = TestingSession()
        yield session
    finally:
        session.close()

app.dependency_overrides[get_session] = overrider_get_session

client = TestClient(app)
