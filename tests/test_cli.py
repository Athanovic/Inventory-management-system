from unittest.mock import patch
import cli


@patch("builtins.input", side_effect=["9"])
@patch("builtins.print")
def test_cli_exit(mock_print, mock_input):
    cli.main()
    mock_print.assert_any_call("Exiting CLI. Goodbye!")


@patch("requests.get")
@patch("builtins.print")
def test_list_inventory(mock_print, mock_get):
    mock_get.return_value.json.return_value = [{"id": 1, "product_name": "Milk"}]

    cli.list_inventory()

    mock_get.assert_called_once_with("http://127.0.0.1:5000/inventory")
    mock_print.assert_called_once()


@patch("requests.post")
@patch("builtins.input", side_effect=["Juice", "BrandX", "4.99", "12", "12345", "Water, fruit"])
@patch("builtins.print")
def test_add_new_item(mock_print, mock_input, mock_post):
    mock_post.return_value.json.return_value = {"message": "created"}

    cli.add_new_item()

    mock_post.assert_called_once()
    mock_print.assert_called_once()


@patch("requests.patch")
@patch("builtins.input", side_effect=["1", "", "", "8.99", "30", "", ""])
@patch("builtins.print")
def test_update_existing_item(mock_print, mock_input, mock_patch):
    mock_patch.return_value.json.return_value = {"message": "updated"}

    cli.update_existing_item()

    mock_patch.assert_called_once()
    mock_print.assert_called_once()



@patch("requests.delete")
@patch("builtins.input", side_effect=["1"])
@patch("builtins.print")
def test_delete_existing_item(mock_print, mock_input, mock_delete):
    mock_delete.return_value.json.return_value = {"message": "deleted"}

    cli.delete_existing_item()

    mock_delete.assert_called_once()
    mock_print.assert_called_once()