from unittest.mock import patch, Mock

from external_api import search_product_by_barcode, search_product_by_name


@patch("external_api.requests.get")
def test_search_product_by_barcode_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar"
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = search_product_by_barcode("737628064502")

    assert result is not None
    assert result["product_name"] == "Organic Almond Milk"
    assert result["brand"] == "Silk"
    assert result["barcode"] == "737628064502"


@patch("external_api.requests.get")
def test_search_product_by_barcode_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"status": 0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = search_product_by_barcode("0000000000")

    assert result is None


@patch("external_api.requests.get")
def test_search_product_by_name_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Peanut Butter",
                "brands": "Skippy",
                "ingredients_text": "Roasted peanuts, sugar",
                "code": "3760011694103"
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = search_product_by_name("peanut butter")

    assert result is not None
    assert result["product_name"] == "Peanut Butter"
    assert result["brand"] == "Skippy"
    assert result["barcode"] == "3760011694103"



@patch("external_api.requests.get")
def test_search_product_by_name_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"products": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = search_product_by_name("unknown product")

    assert result is None