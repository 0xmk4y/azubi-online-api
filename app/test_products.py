import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is called `app`
from unittest.mock import MagicMock

# TestClient is used to interact with the FastAPI app in a test context
client = TestClient(app)

# Mocking the database session and CRUD operations
@pytest.fixture
def mock_db():
    # Here you would mock your database session and CRUD functions
    mock_db_session = MagicMock()
    return mock_db_session

# Test for retrieving all products
def test_read_products(mock_db):
    # Mocking the return value of the `get_products` function
    mock_db.get_products.return_value = [
        {"id": 1, "name": "Product 1", "category": None, "price": 99.99, "images": None},
        {"id": 2, "name": "Product 2", "category": "Category 1", "price": 59.99, "images": None}
    ]

    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Product 1"

# Test for retrieving a product by ID
def test_read_product(mock_db):
    mock_db.get_product_by_id.return_value = {"id": 1, "name": "Product 1", "category": None, "price": 99.99, "images": None}

    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Product 1"

# Test for creating a product (admin required)
def test_create_product(mock_db):
    product_data = {
        "name": "Product 1", 
        "category": "Category 1", 
        "price": 99.99,
        "images": {"image1": "url1.jpg", "image2": "url2.jpg"}
    }

    # Simulate correct admin credentials
    response = client.post(
        "/products",
        json=product_data,
        auth=("admin", "admin")  # Replace with your actual test admin credentials
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Product 1"
    assert response.json()["category"] == "Category 1"
    assert response.json()["price"] == 99.99

# Test for updating a product (admin required)
def test_update_product(mock_db):
    product_data = {
        "name": "Updated Product", 
        "category": "Category 2", 
        "price": 89.99,
        "images": {"image1": "updated_url1.jpg"}
    }
    
    # Simulate correct admin credentials
    mock_db.update_product.return_value = {"id": 1, "name": "Updated Product", "category": "Category 2", "price": 89.99, "images": {"image1": "updated_url1.jpg"}}
    
    response = client.put(
        "/products/1",
        json=product_data,
        auth=("admin", "admin")
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["category"] == "Category 2"
    assert response.json()["price"] == 89.99

# Test for deleting a product (admin required)
def test_delete_product(mock_db):
    mock_db.delete_product.return_value = {"id": 1, "name": "Product to be deleted", "category": "Category 1", "price": 49.99, "images": None}
    
    # Simulate correct admin credentials
    response = client.delete(
        "/products/1",
        auth=("admin", "admin")
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Product to be deleted"

# Test for unauthorized access (invalid admin credentials)
def test_create_product_unauthorized():
    product_data = {
        "name": "Product 1", 
        "category": "Category 1", 
        "price": 99.99,
        "images": {"image1": "url1.jpg"}
    }
    
    response = client.post(
        "/products",
        json=product_data,
        auth=("wrong_username", "wrong_password")
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
