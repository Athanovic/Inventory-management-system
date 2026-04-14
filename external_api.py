import requests

HEADERS = {
    "User-Agent": "Inventory-App/1.0 (learning project)"
}

BASE_PRODUCT_URL = "https://world.openfoodfacts.org/api/v0/product"
BASE_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def search_product_by_barcode(barcode):
    url = f"{BASE_PRODUCT_URL}/{barcode}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "product_name": product.get("product_name"),
            "brand": product.get("brands"),
            "ingredients": product.get("ingredients_text"),
            "barcode": barcode
        }

    except requests.RequestException:
        return None


def search_product_by_name(name):
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    try:
        response = requests.get(
            BASE_SEARCH_URL,
            params=params,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        if not products:
            return None

        product = products[0]

        return {
            "product_name": product.get("product_name"),
            "brand": product.get("brands"),
            "ingredients": product.get("ingredients_text"),
            "barcode": product.get("code")
        }

    except requests.RequestException:
        return None