import pytest
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


def test_add_to_cart_with_negative_quantity_returns_400(clean_cart):
    response = requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": -1},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_add_to_cart_with_very_large_quantity_returns_400(clean_cart):
    response = requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 999999},
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


def test_update_cart_quantity_successfully(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/cart/update",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 3},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    assert "message" in response.json()

    cart_response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)
    item = cart_response.json()["items"][0]
    assert item["quantity"] == 3


def test_update_cart_quantity_below_one_returns_400(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/cart/update",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 0},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_remove_existing_cart_item_succeeds(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/cart/remove",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    assert "message" in response.json()

    cart_response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)
    assert cart_response.json()["items"] == []


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


def test_duplicate_add_accumulates_quantity(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 2},
        timeout=TIMEOUT,
    )

    response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["quantity"] == 3


def test_add_quantity_exceeding_stock_returns_400(clean_cart):
    response = requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 183},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_cart_is_empty_after_clear(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )
    requests.delete(f"{BASE_URL}/cart/clear", headers=request_headers(1), timeout=TIMEOUT)

    response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"] == []
    assert payload["total"] == 0


def test_cart_total_equals_sum_of_item_subtotals(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 2},
        timeout=TIMEOUT,
    )

    response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    subtotal_sum = sum(item["subtotal"] for item in payload["items"])
    assert payload["total"] == pytest.approx(subtotal_sum)


def test_cart_item_subtotal_equals_quantity_times_unit_price(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 2},
        timeout=TIMEOUT,
    )

    response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["subtotal"] == pytest.approx(item["quantity"] * item["unit_price"])


def test_cart_total_includes_last_item_subtotal(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 2, "quantity": 1},
        timeout=TIMEOUT,
    )

    response = requests.get(f"{BASE_URL}/cart", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) >= 2
    expected_total = sum(item["subtotal"] for item in payload["items"])
    assert payload["total"] == pytest.approx(expected_total)
