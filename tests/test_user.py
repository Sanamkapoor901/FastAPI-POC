from tests.base import client, test_user, setup_db

def test_create_user(setup_db):
    # Test creating a new user
    response = client.post("/auth/register/", json=test_user)
    assert response.status_code == 201
    assert response.json()["email"] == test_user["email"]

def test_user_login():
    # Test logging in with the created user credentials
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    response = client.post("/auth/login/", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_login():
    # Test logging in with invalid credentials
    login_data = {"username": test_user["username"], "password": "wrongpassword"}
    response = client.post("/auth/login/", data=login_data)
    assert response.status_code == 401

def test_get_user_profile():
    # Obtain an access token
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    response = client.post("/auth/login/", data=login_data)
    access_token = response.json()["access_token"]

    # Access user profile with token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/user/profile/", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
