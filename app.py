from flask import Flask, jsonify, request
from inventory import inventory, get_next_id
from external_api import fetch_product_by_barcode, fetch_products_by_name

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Inventory Management API"}), 200


# GET /inventory -> Fetch all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


# GET /inventory/<id> -> Fetch a single item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


# POST /inventory -> Add a new item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    required_fields = ["barcode", "product_name", "brand", "ingredients", "price", "stock"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_item = {
        "id": get_next_id(),
        "barcode": data["barcode"],
        "product_name": data["product_name"],
        "brand": data["brand"],
        "ingredients": data["ingredients"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


# PATCH /inventory/<id> -> Update an item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    allowed_fields = ["barcode", "product_name", "brand", "ingredients", "price", "stock"]
    for key, value in data.items():
        if key in allowed_fields:
            item[key] = value

    return jsonify(item), 200


# DELETE /inventory/<id> -> Remove an item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200


# GET /search/barcode/<barcode> -> Fetch product from OpenFoodFacts by barcode
@app.route("/search/barcode/<barcode>", methods=["GET"])
def search_barcode(barcode):
    product = fetch_product_by_barcode(barcode)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


# GET /search/name/<name> -> Search products by name
@app.route("/search/name/<name>", methods=["GET"])
def search_name(name):
    products = fetch_products_by_name(name)
    if not products:
        return jsonify({"error": "No matching products found"}), 404
    return jsonify(products), 200


# POST /inventory/import/<barcode> -> Fetch from API and add to inventory
@app.route("/inventory/import/<barcode>", methods=["POST"])
def import_item_by_barcode(barcode):
    product = fetch_product_by_barcode(barcode)
    if not product:
        return jsonify({"error": "Product not found in external API"}), 404

    new_item = {
        "id": get_next_id(),
        "barcode": barcode,
        "product_name": product.get("product_name", "Unknown Product"),
        "brand": product.get("brands", "Unknown Brand"),
        "ingredients": product.get("ingredients_text", "N/A"),
        "price": 0.0,   # default price
        "stock": 0      # default stock
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)