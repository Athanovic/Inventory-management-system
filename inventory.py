inventory = [
    {
        "id": 1,
        "barcode": "3017624010701",
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds, cane sugar",
        "price": 4.99,
        "stock": 20
    },
    {
        "id": 2,
        "barcode": "737628064502",
        "product_name": "Peanut Butter",
        "brand": "Skippy",
        "ingredients": "Roasted peanuts, sugar, hydrogenated vegetable oil, salt",
        "price": 3.49,
        "stock": 15
    }
]


def get_next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1