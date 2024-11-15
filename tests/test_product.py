from tests.base import client, test_product, test_user, setup_db

def get_token():
    response = client.post("/auth/login/", data=test_user)
    return response.json()["access_token"]


def test_create_product(setup_db):
    token = get_token()
    response = client.post("/product/", json=test_product, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == test_product["name"]

def test_get_product(setup_db):
    token = get_token()
    response = client.get("/products/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["products"][0]["name"] == test_product["name"]

def test_get_all_products(setup_db):
    token = get_token()
    response = client.get("/product/all/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authorized to access this resource"

def test_get_product_by_id(setup_db):
    token = get_token()
    response = client.get("/product/1/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == test_product["name"]

def test_update_product(setup_db):
    token = get_token()
    response = client.put("/product/1/", json=test_product, headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == test_product["name"]

def test_delete_product(setup_db):
    token = get_token()
    response = client.delete("/product/1/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"detail": "Product deleted successfully"}