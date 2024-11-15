import pytest
from main import app
from fastapi.testclient import TestClient
from database import SessionLocal, get_test_db, get_db, Base, test_engine

app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)

# Sample data for testing

test_user = {
    "username": "zeel",
    "email": "zeel@example.com",
    "password": "testpassword"
}


test_product = {
    "name": "Test Product",
    "description": "This is a test product",
    "price": 10.0,
    "quantity": 100
}

@pytest.fixture(scope="module")
def setup_db():
    # Setup database fixture to create tables
    Base.metadata.create_all(bind=test_engine)

    # Create a test user
    client.post("/auth/register/", json=test_user)

    db_session = SessionLocal()
    yield
    # Teardown fixture to drop tables after tests
    db_session.close()
    Base.metadata.drop_all(bind=test_engine)