import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, clean_cart, request_headers


def test_get_cart_returns_expected_structure(clean_cart):
    response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["cart_id", "items", "total"])
    assert isinstance(payload["items"], list)


def test_add_to_cart_returns_success_message(clean_cart):
    response = requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Item added to cart"


def test_add_to_cart_with_zero_quantity_returns_400(clean_cart):
    response = requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 0},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_remove_missing_cart_item_returns_404(clean_cart):
    response = requests.post(
        f"{BASE_URL}/cart/remove",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 999999},
        timeout=TIMEOUT,
    )

    assert response.status_code == 404
    assert "error" in response.json()


def test_clear_cart_returns_success_message(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )

    response = requests.delete(f"{BASE_URL}/cart/clear", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    assert "message" in response.json()
