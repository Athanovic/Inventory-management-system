import copy

import pytest

import app as app_module
import inventory as inventory_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    original = copy.deepcopy(inventory_module.inventory)
    yield
    inventory_module.inventory.clear()
    inventory_module.inventory.extend(original)


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory Management System API is running"


def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_single_inventory_item_found(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_single_inventory_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"


def test_create_inventory_item(client):
    payload = {
        "product_name": "Apple Juice",
        "brand": "Tropicana",
        "price": 6.50,
        "stock": 10,
        "barcode": "111222333"
    }

    response = client.post("/inventory", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data["product_name"] == "Apple Juice"
    assert data["brand"] == "Tropicana"


def test_patch_inventory_item(client):
    payload = {
        "price": 9.99,
        "stock": 50
    }

    response = client.patch("/inventory/1", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["price"] == 9.99
    assert data["stock"] == 50


def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Item deleted successfully"


def test_search_by_barcode_route(client, monkeypatch):
    def mock_search_product_by_barcode(barcode):
        return {
            "status": 1,
            "product_name": "Mock Almond Milk",
            "brand": "Mock Brand",
            "ingredients": "Water, almonds",
            "barcode": barcode
        }

    monkeypatch.setattr(app_module, "search_product_by_barcode", mock_search_product_by_barcode)

    response = client.get("/search/barcode/123456")
    data = response.get_json()

    assert response.status_code == 200
    assert data["product_name"] == "Mock Almond Milk"


def test_search_by_name_route(client, monkeypatch):
    def mock_search_product_by_name(name):
        return {
            "status": 1,
            "product_name": "Mock Peanut Butter",
            "brand": "Mock Brand",
            "ingredients": "Peanuts, salt",
            "barcode": "999999"
        }

    monkeypatch.setattr(app_module, "search_product_by_name", mock_search_product_by_name)

    response = client.get("/search/name/peanut")
    data = response.get_json()

    assert response.status_code == 200
    assert data["product_name"] == "Mock Peanut Butter"


def test_import_product_by_barcode(client, monkeypatch):
    def mock_search_product_by_barcode(barcode):
        return {
            "status": 1,
            "product_name": "Imported Product",
            "brand": "Imported Brand",
            "ingredients": "Imported ingredients",
            "barcode": barcode
        }

    monkeypatch.setattr(app_module, "search_product_by_barcode", mock_search_product_by_barcode)

    response = client.post("/import/barcode/555555")
    data = response.get_json()

    assert response.status_code == 201
    assert data["product_name"] == "Imported Product"
    assert data["barcode"] == "555555"