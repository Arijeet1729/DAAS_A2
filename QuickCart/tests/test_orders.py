import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


def test_get_orders_returns_order_list():
    response = requests.get(f"{BASE_URL}/orders", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(payload[0], ["order_id", "total_amount", "payment_status", "order_status"])


def test_get_order_detail_returns_items_and_statuses():
    orders = requests.get(f"{BASE_URL}/orders", headers=request_headers(1), timeout=TIMEOUT).json()
    order_id = orders[0]["order_id"]

    response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["order_id", "items", "total_amount", "payment_status", "order_status"])
    assert isinstance(payload["items"], list)


def test_get_invoice_returns_expected_fields():
    orders = requests.get(f"{BASE_URL}/orders", headers=request_headers(1), timeout=TIMEOUT).json()
    order_id = orders[0]["order_id"]

    response = requests.get(
        f"{BASE_URL}/orders/{order_id}/invoice",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["gst_amount", "order_id", "subtotal", "total_amount"])


def test_get_unknown_order_returns_404():
    response = requests.get(f"{BASE_URL}/orders/999999", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 404
    assert "error" in response.json()
