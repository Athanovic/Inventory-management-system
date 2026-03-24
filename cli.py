import requests

BASE_URL = "http://127.0.0.1:5000"


def list_inventory():
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        items = response.json()
        print("\n--- Inventory Items ---")
        for item in items:
            print(item)
    else:
        print("Failed to fetch inventory.")


def get_item():
    item_id = input("Enter item ID: ")
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("Item not found.")


def add_item():
    print("\n--- Add New Item ---")
    data = {
        "barcode": input("Barcode: "),
        "product_name": input("Product name: "),
        "brand": input("Brand: "),
        "ingredients": input("Ingredients: "),
        "price": float(input("Price: ")),
        "stock": int(input("Stock: "))
    }

    response = requests.post(f"{BASE_URL}/inventory", json=data)
    if response.status_code == 201:
        print("Item added successfully:")
        print(response.json())
    else:
        print("Failed to add item:", response.json())


def update_item():
    item_id = input("Enter item ID to update: ")
    print("\nLeave blank if you do not want to change a field.")

    data = {}
    barcode = input("New barcode: ")
    product_name = input("New product name: ")
    brand = input("New brand: ")
    ingredients = input("New ingredients: ")
    price = input("New price: ")
    stock = input("New stock: ")

    if barcode:
        data["barcode"] = barcode
    if product_name:
        data["product_name"] = product_name
    if brand:
        data["brand"] = brand
    if ingredients:
        data["ingredients"] = ingredients
    if price:
        data["price"] = float(price)
    if stock:
        data["stock"] = int(stock)

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
    if response.status_code == 200:
        print("Item updated successfully:")
        print(response.json())
    else:
        print("Failed to update item:", response.json())


def delete_item():
    item_id = input("Enter item ID to delete: ")
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Failed to delete item.")


def search_barcode():
    barcode = input("Enter barcode: ")
    response = requests.get(f"{BASE_URL}/search/barcode/{barcode}")
    if response.status_code == 200:
        print("\n--- Product Found ---")
        print(response.json())
    else:
        print("Product not found in external API.")


def search_name():
    name = input("Enter product name: ")
    response = requests.get(f"{BASE_URL}/search/name/{name}")
    if response.status_code == 200:
        print("\n--- Search Results ---")
        for product in response.json():
            print(product)
    else:
        print("No matching products found.")


def import_barcode():
    barcode = input("Enter barcode to import: ")
    response = requests.post(f"{BASE_URL}/inventory/import/{barcode}")
    if response.status_code == 201:
        print("Product imported successfully:")
        print(response.json())
    else:
        print("Failed to import product:", response.json())


def menu():
    while True:
        print("\n=== Inventory Management CLI ===")
        print("1. List inventory")
        print("2. View single item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search product by barcode")
        print("7. Search product by name")
        print("8. Import product by barcode into inventory")
        print("9. Exit")

        choice = input("Choose an option (1-9): ")

        if choice == "1":
            list_inventory()
        elif choice == "2":
            get_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_barcode()
        elif choice == "7":
            search_name()
        elif choice == "8":
            import_barcode()
        elif choice == "9":
            print("Exiting CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()