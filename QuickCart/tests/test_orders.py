import requests
from requests.exceptions import ReadTimeout

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
    assert round(float(payload["subtotal"]) + float(payload["gst_amount"]), 2) == round(
        float(payload["total_amount"]), 2
    )


def test_get_unknown_order_returns_404():
    response = requests.get(f"{BASE_URL}/orders/999999", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 404
    assert "error" in response.json()


def test_cancel_delivered_order_returns_400():
    try:
        response = requests.post(
            f"{BASE_URL}/orders/2038/cancel",
            headers=request_headers(1),
            timeout=TIMEOUT,
        )
    except ReadTimeout:
        assert False, "Delivered order cancel timed out instead of returning 400"

    assert response.status_code == 400
    assert "error" in response.json()


def test_cancel_order_without_roll_number_returns_401():
    response = requests.post(
        f"{BASE_URL}/orders/1209/cancel",
        headers={"X-User-ID": "1"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 401
    assert "error" in response.json()


def test_cancel_order_without_user_id_returns_400():
    response = requests.post(
        f"{BASE_URL}/orders/1209/cancel",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_get_order_detail_without_roll_number_returns_401():
    response = requests.get(f"{BASE_URL}/orders/1209", headers={"X-User-ID": "1"}, timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()


def test_get_order_detail_without_user_id_returns_400():
    response = requests.get(
        f"{BASE_URL}/orders/1209",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_get_invoice_with_invalid_order_id_returns_404():
    response = requests.get(
        f"{BASE_URL}/orders/999999/invoice",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert response.status_code == 404
    assert "error" in response.json()


def test_get_invoice_without_roll_number_returns_401():
    response = requests.get(
        f"{BASE_URL}/orders/1209/invoice",
        headers={"X-User-ID": "1"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 401
    assert "error" in response.json()


def test_get_invoice_without_user_id_returns_400():
    response = requests.get(
        f"{BASE_URL}/orders/1209/invoice",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_successful_cancel_restores_stock():
    before_product = requests.get(
        f"{BASE_URL}/products/1",
        headers=request_headers(1),
        timeout=TIMEOUT,
    ).json()
    before_stock = before_product["stock_quantity"]

    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )
    checkout_response = requests.post(
        f"{BASE_URL}/checkout",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"payment_method": "CARD"},
        timeout=TIMEOUT,
    )
    created_order_id = checkout_response.json()["order_id"]

    cancel_response = requests.post(
        f"{BASE_URL}/orders/{created_order_id}/cancel",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert cancel_response.status_code == 200
    assert "message" in cancel_response.json()

    after_product = requests.get(
        f"{BASE_URL}/products/1",
        headers=request_headers(1),
        timeout=TIMEOUT,
    ).json()
    assert after_product["stock_quantity"] == before_stock
