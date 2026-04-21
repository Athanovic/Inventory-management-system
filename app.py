print("🔥 CORRECT APP IS RUNNING")

from flask import Flask, jsonify, request

from inventory import inventory, get_all_items, get_item_by_id, add_item, update_item, delete_item
from external_api import search_product_by_barcode, search_product_by_name

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Inventory Management System API is running"}), 200


# =========================
# CRUD ROUTES
# =========================

@app.route("/inventory", methods=["GET"])
def fetch_inventory():
    return jsonify(get_all_items()), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def fetch_single_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ["product_name", "brand", "price", "stock", "barcode"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        data["price"] = float(data["price"])
        data["stock"] = int(data["stock"])
    except (ValueError, TypeError):
        return jsonify({"error": "Price must be a number and stock must be an integer"}), 400

    new_item = add_item(data)
    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    if "price" in data:
        try:
            data["price"] = float(data["price"])
        except (ValueError, TypeError):
            return jsonify({"error": "Price must be a number"}), 400

    if "stock" in data:
        try:
            data["stock"] = int(data["stock"])
        except (ValueError, TypeError):
            return jsonify({"error": "Stock must be an integer"}), 400

    updated = update_item(item_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    deleted = delete_item(item_id)
    if deleted:
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"error": "Item not found"}), 404


# =========================
# HELPER ROUTES (EXTERNAL API)
# =========================

@app.route("/search/barcode/<barcode>", methods=["GET"])
def search_by_barcode(barcode):
    product = search_product_by_barcode(barcode)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found from external API"}), 404


@app.route("/search/name/<name>", methods=["GET"])
def search_by_name(name):
    product = search_product_by_name(name)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found from external API"}), 404


@app.route('/inventory/import/<barcode>', methods=['POST'])
def import_product_by_barcode(barcode):

    if not product:
        return jsonify({"error": "Product not found from external API"}), 404

    new_item = {
        "product_name": product.get("product_name", "Unknown Product"),
        "brand": product.get("brand", "Unknown Brand"),
        "price": 0.0,  # default placeholder price
        "stock": 0,    # default placeholder stock
        "barcode": barcode,
        "ingredients": product.get("ingredients", "")
    }

    created_item = add_item(new_item)
    return jsonify(created_item), 201


print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)