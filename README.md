# Inventory Management System (Flask REST API)

## Project Overview
This project is a Flask-based Inventory Management System for a small retail company.

It includes:
- Full CRUD operations for inventory items
- External API integration with OpenFoodFacts
- CLI interface for interacting with the API
- Unit tests using pytest and unittest.mock

---

## Features

### Flask REST API Routes
- `GET /` → API status check
- `GET /inventory` → Fetch all inventory items
- `GET /inventory/<id>` → Fetch a single inventory item
- `POST /inventory` → Add a new inventory item
- `PATCH /inventory/<id>` → Update an inventory item
- `DELETE /inventory/<id>` → Delete an inventory item

### External API Helper Routes
- `GET /search/barcode/<barcode>` → Search product from OpenFoodFacts by barcode
- `GET /search/name/<name>` → Search product from OpenFoodFacts by product name
- `POST /import/barcode/<barcode>` → Import product from OpenFoodFacts into inventory array

### CLI Interface
- List inventory
- View single item
- Add item
- Update item
- Delete item
- Search product by barcode
- Search product by name
- Import product by barcode into inventory

### Testing
- API endpoint tests
- CLI tests
- External API tests
- Mocked API responses using unittest.mock

## Requirements
- Python 3.10+
- pip
- Flask
- requests
- pytest