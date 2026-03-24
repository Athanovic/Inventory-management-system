import requests

BARCODE_URL = "https://world.openfoodfacts.org/api/v2/product/{}.json"
SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def fetch_product_by_barcode(barcode):
    try:
        response = requests.get(BARCODE_URL.format(barcode), timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == 1:
            return data.get("product", {})
        return None

    except requests.RequestException:
        return None


def fetch_products_by_name(name):
    try:
        params = {
            "search_terms": name,
            "search_simple": 1,
            "action": "process",
            "json": 1
        }
        response = requests.get(SEARCH_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        products = data.get("products", [])
        results = []

        for product in products[:5]:  # limit to first 5 results
            results.append({
                "product_name": product.get("product_name", "Unknown Product"),
                "brands": product.get("brands", "Unknown Brand"),
                "ingredients_text": product.get("ingredients_text", "N/A"),
                "code": product.get("code", "N/A")
            })

        return results

    except requests.RequestException:
        return []