# Inventory Management System (Flask REST API + CLI)

## Project Overview
This project is a Python Flask-based Inventory Management System for a small retail company.

It includes:
- A Flask REST API with CRUD operations
- OpenFoodFacts external API integration
- A CLI tool to interact with the API
- Unit tests using pytest and unittest.mock

---

## Features
- Flask REST API includes full CRUD operations for inventory management



### REST API Endpoints
- `GET /` → Welcome route
- `GET /inventory` → Fetch all inventory items
- `GET /inventory/<id>` → Fetch a single item
- `POST /inventory` → Add a new item
- `PATCH /inventory/<id>` → Update an item
- `DELETE /inventory/<id>` → Delete an item
- `GET /search/barcode/<barcode>` → Search OpenFoodFacts by barcode
- `GET /search/name/<name>` → Search OpenFoodFacts by product name
- `POST /inventory/import/<barcode>` → Import product from OpenFoodFacts into inventory

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd inventory-management-system