import requests

BASE_URL = "http://127.0.0.1:5000"


def safe_print(response):
    try:
        print(response.json())
    except:
        print("Error:", response.text)


def list_inventory():
    res = requests.get(f"{BASE_URL}/inventory")
    safe_print(res)


def view_single_item():
    item_id = input("Enter item ID: ")
    res = requests.get(f"{BASE_URL}/inventory/{item_id}")
    safe_print(res)


def add_new_item():
    name = input("Product name: ")
    brand = input("Brand: ")
    price = input("Price: ")
    stock = input("Stock: ")
    barcode = input("Barcode: ")
    ingredients = input("Ingredients: ")

    try:
        price = float(price)
        stock = int(stock)
    except:
        print("Invalid input")
        return

    data = {
        "product_name": name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "barcode": barcode,
        "ingredients": ingredients
    }

    res = requests.post(f"{BASE_URL}/inventory", json=data)
    safe_print(res)


def update_existing_item():
    item_id = input("Enter item ID: ")

    data = {}

    price = input("New price: ")
    if price:
        data["price"] = float(price)

    stock = input("New stock: ")
    if stock:
        data["stock"] = int(stock)

    res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
    safe_print(res)


def delete_existing_item():
    item_id = input("Enter item ID: ")
    res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    safe_print(res)


def search_barcode():
    barcode = input("Enter barcode: ")
    res = requests.get(f"{BASE_URL}/search/barcode/{barcode}")
    safe_print(res)


def search_name():
    name = input("Enter name: ")
    res = requests.get(f"{BASE_URL}/search/name/{name}")
    safe_print(res)


def import_barcode():
    barcode = input("Enter barcode: ")
    res = requests.post(f"{BASE_URL}/inventory/import/{barcode}")
    safe_print(res)


def main():
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
            print("Invalid choice")


if __name__ == "__main__":
    main()