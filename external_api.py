import requests

BASE_PRODUCT_URL = "https://world.openfoodfacts.org/api/v0/product"
BASE_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def search_product_by_barcode(barcode):
    """
    Fetch a product by barcode from OpenFoodFacts.
    Returns a simplified product dict or None if not found.
    """
    url = f"{BASE_PRODUCT_URL}/{barcode}.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != 1 or "product" not in data:
            return None

        product = data["product"]

        return {
            "status": data.get("status", 0),
            "product_name": product.get("product_name", "Unknown Product"),
            "brand": product.get("brands", "Unknown Brand"),
            "ingredients": product.get("ingredients_text", ""),
            "barcode": barcode
        }

    except (requests.RequestException, ValueError):
        return None


def search_product_by_name(name):
    """
    Search a product by name from OpenFoodFacts.
    Returns the first matching simplified product dict or None.
    """
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    try:
        response = requests.get(BASE_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        products = data.get("products", [])
        if not products:
            return None

        product = products[0]

        return {
            "status": 1,
            "product_name": product.get("product_name", "Unknown Product"),
            "brand": product.get("brands", "Unknown Brand"),
            "ingredients": product.get("ingredients_text", ""),
            "barcode": product.get("code", "")
        }


    except (requests.RequestException, ValueError):
        return None