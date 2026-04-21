inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 5.99,
        "stock": 20,
        "barcode": "737628064502",
        "ingredients": "Filtered water, almonds, cane sugar"
    },
    {
        "id": 2,
        "product_name": "Peanut Butter",
        "brand": "Skippy",
        "price": 4.49,
        "stock": 15,
        "barcode": "3760011694103",
        "ingredients": "Roasted peanuts, sugar, palm oil, salt"
    }
]


def get_next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


def get_all_items():
    return inventory


def get_item_by_id(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


def add_item(data):
    new_item = {
        "id": get_next_id(),
        "product_name": data.get("product_name", "Unknown Product"),
        "brand": data.get("brand", "Unknown Brand"),
        "price": float(data.get("price", 0.0)),
        "stock": int(data.get("stock", 0)),
        "barcode": data.get("barcode", ""),
        "ingredients": data.get("ingredients", "")
    }
    inventory.append(new_item)
    return new_item


def update_item(item_id, updates):
    item = get_item_by_id(item_id)
    if not item:
        return None

    allowed_fields = ["product_name", "brand", "price", "stock", "barcode", "ingredients"]
    for key, value in updates.items():
        if key in allowed_fields:
            item[key] = value

    return item



def delete_item(item_id):
    item = get_item_by_id(item_id)
    if not item:
        return False

    inventory.remove(item)
    return True



