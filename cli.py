import requests


BASE_URL = "http://127.0.0.1:5000"


def print_menu():
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


def list_inventory():
    response = requests.get(f"{BASE_URL}/inventory")
    print(response.json())


def view_single_item():
    item_id = input("Enter item ID: ")
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    print(response.json())


def add_new_item():
    product_name = input("Product name: ")
    brand = input("Brand: ")
    price = input("Price: ")
    stock = input("Stock: ")
    barcode = input("Barcode: ")
    ingredients = input("Ingredients (optional): ")

    payload = {
        "product_name": product_name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "barcode": barcode,
        "ingredients": ingredients
    }

    response = requests.post(f"{BASE_URL}/inventory", json=payload)
    print(response.json())


def update_existing_item():
    item_id = input("Enter item ID to update: ")

    print("Leave blank if you don't want to change a field.")
    product_name = input("New product name: ")
    brand = input("New brand: ")
    price = input("New price: ")
    stock = input("New stock: ")
    barcode = input("New barcode: ")
    ingredients = input("New ingredients: ")

    updates = {}

    if product_name:
        updates["product_name"] = product_name
    if brand:
        updates["brand"] = brand
    if price:
        updates["price"] = price
    if stock:
        updates["stock"] = stock
    if barcode:
        updates["barcode"] = barcode
    if ingredients:
        updates["ingredients"] = ingredients

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=updates)
    print(response.json())


def delete_existing_item():
    item_id = input("Enter item ID to delete: ")
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print(response.json())


def search_barcode():
    barcode = input("Enter barcode: ")
    response = requests.get(f"{BASE_URL}/search/barcode/{barcode}")
    print(response.json())


def search_name():
    name = input("Enter product name: ")
    response = requests.get(f"{BASE_URL}/search/name/{name}")
    print(response.json())


def import_barcode():
    barcode = input("Enter barcode to import: ")
    response = requests.post(f"{BASE_URL}/import/barcode/{barcode}")
    print(response.json())


def main():
    while True:
        print_menu()
        choice = input("Choose an option (1-9): ")

        if choice == "1":
            list_inventory()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_new_item()
        elif choice == "4":
            update_existing_item()
        elif choice == "5":
            delete_existing_item()
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
            print("Invalid option. Please choose between 1 and 9.")


if __name__ == "__main__":
    main()