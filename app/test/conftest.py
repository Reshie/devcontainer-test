import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database
from app.database import Base

@pytest.fixture(scope="function")
def SessionLocal():
    TEST_SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres_temp"
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

    assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield SessionLocal
    
    drop_database(TEST_SQLALCHEMY_DATABASE_URL)