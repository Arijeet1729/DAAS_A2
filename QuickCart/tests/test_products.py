import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


def test_get_products_returns_active_product_list():
    response = requests.get(f"{BASE_URL}/products", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(payload[0], ["product_id", "name", "category", "price", "stock_quantity", "is_active"])
    assert payload[0]["is_active"] is True


def test_get_single_product_returns_expected_fields():
    response = requests.get(f"{BASE_URL}/products/1", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["product_id", "name", "category", "price", "stock_quantity", "is_active"])
    assert payload["product_id"] == 1


def test_get_missing_product_returns_404():
    response = requests.get(f"{BASE_URL}/products/999999", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 404
    assert "error" in response.json()


def test_get_products_without_user_id_returns_400():
    response = requests.get(
        f"{BASE_URL}/products",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()
