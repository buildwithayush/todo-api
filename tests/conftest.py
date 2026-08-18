import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./test_temp.db'

engine = create_engine(
  SQL_ALCHEMY_DATABASE_URL,
  connect_args={'check_same_thread':False}
)

TestingSessionLocal = sessionmaker(autocommit= False,autoflush=False,bind=engine)

def overridden_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
      db.close()

@pytest.fixture(scope='session',autouse=True)
def setup_database():
   Base.metadata.create_all(bind=engine)
  
   yield
   Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
   app.dependency_overrides[get_db] = overridden_get_db
   with TestClient(app) as test_client:
      yield test_client
   app.dependency_overrides.clear()   

      


